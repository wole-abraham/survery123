import threading
import logging
import os
from django.conf import settings
from .file_upload_utils import upload_file_to_gdrive, create_photo_record, create_video_record, upload_file_to_gdrive_from_content
from .models import ActivityPhoto, ActivityVideo

logger = logging.getLogger(__name__)

def upload_files_to_gdrive_background(activity, uploaded_files):
    """
    Background task to upload files to Google Drive
    
    Args:
        activity: Activities instance
        uploaded_files: List of tuples (file, file_type) where file_type is 'photo' or 'video'
    """
    def upload_task():
        try:
            for file, file_type in uploaded_files:
                try:
                    # Upload to Google Drive
                    gdrive_info = upload_file_to_gdrive(file, activity.id, file_type)
                    
                    if gdrive_info:
                        # Update the existing record with Google Drive info and delete local file
                        if file_type == 'photo':
                            photo = ActivityPhoto.objects.filter(
                                activity=activity, 
                                image__isnull=False
                            ).first()
                            if photo:
                                # Store local file path before deleting
                                local_file_path = photo.image.path if photo.image else None
                                
                                # Update with Google Drive info
                                photo.gdrive_file_id = gdrive_info.get('file_id')
                                photo.gdrive_web_view_link = gdrive_info.get('web_view_link')
                                photo.gdrive_web_content_link = gdrive_info.get('web_content_link')
                                photo.gdrive_file_name = gdrive_info.get('file_name')
                                
                                # Clear the local file field
                                photo.image = None
                                photo.save()
                                
                                # Delete the local file
                                if local_file_path and os.path.exists(local_file_path):
                                    try:
                                        os.remove(local_file_path)
                                        logger.info(f"Deleted local photo file: {local_file_path}")
                                    except Exception as e:
                                        logger.error(f"Failed to delete local photo file {local_file_path}: {str(e)}")
                                
                                logger.info(f"Updated photo record with Google Drive info: {file.name}")
                        else:  # video
                            video = ActivityVideo.objects.filter(
                                activity=activity, 
                                video__isnull=False
                            ).first()
                            if video:
                                # Store local file path before deleting
                                local_file_path = video.video.path if video.video else None
                                
                                # Update with Google Drive info
                                video.gdrive_file_id = gdrive_info.get('file_id')
                                video.gdrive_web_view_link = gdrive_info.get('web_view_link')
                                video.gdrive_web_content_link = gdrive_info.get('web_content_link')
                                video.gdrive_file_name = gdrive_info.get('file_name')
                                
                                # Clear the local file field
                                video.video = None
                                video.save()
                                
                                # Delete the local file
                                if local_file_path and os.path.exists(local_file_path):
                                    try:
                                        os.remove(local_file_path)
                                        logger.info(f"Deleted local video file: {local_file_path}")
                                    except Exception as e:
                                        logger.error(f"Failed to delete local video file {local_file_path}: {str(e)}")
                                
                                logger.info(f"Updated video record with Google Drive info: {file.name}")
                    else:
                        logger.warning(f"Google Drive upload failed for {file.name}, keeping local file")
                        
                except Exception as e:
                    logger.error(f"Error uploading {file.name} to Google Drive: {str(e)}")
                    # Keep the local file as fallback
                    
        except Exception as e:
            logger.error(f"Background upload task failed: {str(e)}")
    
    # Start the background task
    thread = threading.Thread(target=upload_task)
    thread.daemon = True
    thread.start()
    logger.info(f"Started background upload task for activity {activity.id}")

def process_uploaded_files_direct_to_gdrive(activity, photo_files, video_files):
    """
    Process uploaded files directly to Google Drive without local storage
    
    Args:
        activity: Activities instance
        photo_files: List of uploaded photo files
        video_files: List of uploaded video files
    """
    # Synchronous version: process uploads and DB creation in main thread
    if not getattr(settings, 'GOOGLE_DRIVE_ENABLED', False):
        logger.info("Google Drive integration disabled or no files to upload")
        return

    # Process photos
    for file in photo_files:
        try:
            file.seek(0)
            file_content = file.read()
            gdrive_info = upload_file_to_gdrive_from_content(file_content, file.name, activity.id, 'photo')
            if gdrive_info:
                ActivityPhoto.objects.create(
                    activity=activity,
                    gdrive_file_id=gdrive_info.get('file_id'),
                    gdrive_web_view_link=gdrive_info.get('web_view_link'),
                    gdrive_web_content_link=gdrive_info.get('web_content_link'),
                    gdrive_file_name=gdrive_info.get('file_name')
                )
                logger.info(f"Created photo record with Google Drive info: {file.name}")
            else:
                logger.error(f"Failed to upload photo to Google Drive: {file.name}")
        except Exception as e:
            logger.error(f"Error uploading photo {file.name} to Google Drive: {str(e)}")

    # Process videos
    for file in video_files:
        try:
            file.seek(0)
            file_content = file.read()
            gdrive_info = upload_file_to_gdrive_from_content(file_content, file.name, activity.id, 'video')
            if gdrive_info:
                ActivityVideo.objects.create(
                    activity=activity,
                    gdrive_file_id=gdrive_info.get('file_id'),
                    gdrive_web_view_link=gdrive_info.get('web_view_link'),
                    gdrive_web_content_link=gdrive_info.get('web_content_link'),
                    gdrive_file_name=gdrive_info.get('file_name')
                )
                logger.info(f"Created video record with Google Drive info: {file.name}")
            else:
                logger.error(f"Failed to upload video to Google Drive: {file.name}")
        except Exception as e:
            logger.error(f"Error uploading video {file.name} to Google Drive: {str(e)}")
