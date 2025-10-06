from django.core.management.base import BaseCommand, CommandError
import os
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Clean up local files that have been uploaded to Google Drive'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        from activities_report.models import ActivityPhoto, ActivityVideo
        
        dry_run = options.get('dry_run', False)
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No files will be deleted'))
        
        # Clean up photos
        photos_with_gdrive = ActivityPhoto.objects.filter(
            gdrive_file_id__isnull=False,
            image__isnull=False
        )
        
        photo_count = 0
        for photo in photos_with_gdrive:
            if photo.image and hasattr(photo.image, 'path'):
                local_path = photo.image.path
                if os.path.exists(local_path):
                    if dry_run:
                        self.stdout.write(f"Would delete photo: {local_path}")
                    else:
                        try:
                            os.remove(local_path)
                            photo.image = None
                            photo.save()
                            self.stdout.write(f"Deleted photo: {local_path}")
                            photo_count += 1
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(f"Failed to delete {local_path}: {str(e)}")
                            )
        
        # Clean up videos
        videos_with_gdrive = ActivityVideo.objects.filter(
            gdrive_file_id__isnull=False,
            video__isnull=False
        )
        
        video_count = 0
        for video in videos_with_gdrive:
            if video.video and hasattr(video.video, 'path'):
                local_path = video.video.path
                if os.path.exists(local_path):
                    if dry_run:
                        self.stdout.write(f"Would delete video: {local_path}")
                    else:
                        try:
                            os.remove(local_path)
                            video.video = None
                            video.save()
                            self.stdout.write(f"Deleted video: {local_path}")
                            video_count += 1
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(f"Failed to delete {local_path}: {str(e)}")
                            )
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'DRY RUN: Would delete {photo_count} photos and {video_count} videos')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {photo_count} photos and {video_count} videos')
            )
