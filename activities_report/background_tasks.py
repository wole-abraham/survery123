import threading
import logging
from django.conf import settings
from .file_upload_utils import upload_file_to_gdrive, create_photo_record, create_video_record
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
                        # Update the existing record with Google Drive info
                        if file_type == 'photo':
                            photo = ActivityPhoto.objects.filter(
                                activity=activity, 
                                image__isnull=False
                            ).first()
                            if photo:
                                photo.gdrive_file_id = gdrive_info.get('file_id')
                                photo.gdrive_web_view_link = gdrive_info.get('web_view_link')
                                photo.gdrive_web_content_link = gdrive_info.get('web_content_link')
                                photo.gdrive_file_name = gdrive_info.get('file_name')
                                photo.save()
                                logger.info(f"Updated photo record with Google Drive info: {file.name}")
                        else:  # video
                            video = ActivityVideo.objects.filter(
                                activity=activity, 
                                video__isnull=False
                            ).first()
                            if video:
                                video.gdrive_file_id = gdrive_info.get('file_id')
                                video.gdrive_web_view_link = gdrive_info.get('web_view_link')
                                video.gdrive_web_content_link = gdrive_info.get('web_content_link')
                                video.gdrive_file_name = gdrive_info.get('file_name')
                                video.save()
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

def process_uploaded_files_background(activity, photo_files, video_files):
    """
    Process uploaded files in the background
    
    Args:
        activity: Activities instance
        photo_files: List of uploaded photo files
        video_files: List of uploaded video files
    """
    # First, create local records immediately for fast response
    uploaded_files = []
    
    # Create photo records
    for file in photo_files:
        photo = ActivityPhoto.objects.create(activity=activity, image=file)
        uploaded_files.append((file, 'photo'))
        logger.info(f"Created local photo record: {file.name}")
    
    # Create video records
    for file in video_files:
        video = ActivityVideo.objects.create(activity=activity, video=file)
        uploaded_files.append((file, 'video'))
        logger.info(f"Created local video record: {file.name}")
    
    # Start background upload to Google Drive
    if uploaded_files and getattr(settings, 'GOOGLE_DRIVE_ENABLED', False):
        upload_files_to_gdrive_background(activity, uploaded_files)
    else:
        logger.info("Google Drive integration disabled or no files to upload")
