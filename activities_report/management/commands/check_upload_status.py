from django.core.management.base import BaseCommand, CommandError
from activities_report.models import ActivityPhoto, ActivityVideo

class Command(BaseCommand):
    help = 'Check the status of file uploads'

    def handle(self, *args, **options):
        # Check photos
        photos = ActivityPhoto.objects.all()
        self.stdout.write(f"Total Photos: {photos.count()}")
        
        for photo in photos:
            self.stdout.write(f"  Photo ID: {photo.id}")
            self.stdout.write(f"    Activity: {photo.activity.id}")
            self.stdout.write(f"    Local file: {photo.image.name if photo.image else 'None'}")
            self.stdout.write(f"    Google Drive ID: {photo.gdrive_file_id or 'None'}")
            self.stdout.write(f"    Google Drive Name: {photo.gdrive_file_name or 'None'}")
            self.stdout.write(f"    View Link: {photo.gdrive_web_view_link or 'None'}")
            self.stdout.write("")
        
        # Check videos
        videos = ActivityVideo.objects.all()
        self.stdout.write(f"Total Videos: {videos.count()}")
        
        for video in videos:
            self.stdout.write(f"  Video ID: {video.id}")
            self.stdout.write(f"    Activity: {video.activity.id}")
            self.stdout.write(f"    Local file: {video.video.name if video.video else 'None'}")
            self.stdout.write(f"    Google Drive ID: {video.gdrive_file_id or 'None'}")
            self.stdout.write(f"    Google Drive Name: {video.gdrive_file_name or 'None'}")
            self.stdout.write(f"    View Link: {video.gdrive_web_view_link or 'None'}")
            self.stdout.write("")
