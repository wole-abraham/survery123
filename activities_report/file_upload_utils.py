import os
import tempfile
import logging
from django.conf import settings
from django.core.files.storage import default_storage
from .gdrive_service import get_gdrive_service

logger = logging.getLogger(__name__)

def upload_file_to_gdrive(file, activity_id, file_type='photo'):
    """
    Upload a file to Google Drive and return the file information
    
    Args:
        file: Django uploaded file object
        activity_id: ID of the activity this file belongs to
        file_type: Type of file ('photo' or 'video')
    
    Returns:
        dict: Contains Google Drive file information or None if upload fails
    """
    try:
        # Check if Google Drive is enabled
        if not getattr(settings, 'GOOGLE_DRIVE_ENABLED', False):
            logger.info("Google Drive integration is disabled")
            return None
        
        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as temp_file:
            # Write the uploaded file content to temporary file
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        try:
            # Generate a unique filename for Google Drive
            file_extension = os.path.splitext(file.name)[1]
            gdrive_filename = f"activity_{activity_id}_{file_type}_{file.name}"
            
            # Upload to Google Drive
            gdrive_service = get_gdrive_service()
            gdrive_info = gdrive_service.upload_file(
                file_path=temp_file_path,
                file_name=gdrive_filename
            )
            
            logger.info(f"Successfully uploaded {file.name} to Google Drive")
            return gdrive_info
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except OSError:
                logger.warning(f"Could not delete temporary file: {temp_file_path}")
                
    except Exception as e:
        logger.error(f"Error uploading file to Google Drive: {str(e)}")
        return None

def create_photo_record(activity, file, gdrive_info=None):
    """
    Create an ActivityPhoto record with Google Drive information
    
    Args:
        activity: Activities instance
        file: Django uploaded file object
        gdrive_info: Google Drive file information dict
    
    Returns:
        ActivityPhoto instance
    """
    from .models import ActivityPhoto
    
    photo = ActivityPhoto(activity=activity)
    
    if gdrive_info:
        # Store Google Drive information
        photo.gdrive_file_id = gdrive_info.get('file_id')
        photo.gdrive_web_view_link = gdrive_info.get('web_view_link')
        photo.gdrive_web_content_link = gdrive_info.get('web_content_link')
        photo.gdrive_file_name = gdrive_info.get('file_name')
    else:
        # Fallback to local storage
        photo.image = file
    
    photo.save()
    return photo

def create_video_record(activity, file, gdrive_info=None):
    """
    Create an ActivityVideo record with Google Drive information
    
    Args:
        activity: Activities instance
        file: Django uploaded file object
        gdrive_info: Google Drive file information dict
    
    Returns:
        ActivityVideo instance
    """
    from .models import ActivityVideo
    
    video = ActivityVideo(activity=activity)
    
    if gdrive_info:
        # Store Google Drive information
        video.gdrive_file_id = gdrive_info.get('file_id')
        video.gdrive_web_view_link = gdrive_info.get('web_view_link')
        video.gdrive_web_content_link = gdrive_info.get('web_content_link')
        video.gdrive_file_name = gdrive_info.get('file_name')
    else:
        # Fallback to local storage
        video.video = file
    
    video.save()
    return video
