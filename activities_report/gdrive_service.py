import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class GoogleDriveService:
    def __init__(self):
        self.service = None
        self.folder_id = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Drive service with service account credentials"""
        try:
            # Get the path to the service account JSON file
            credentials_path = getattr(settings, 'GOOGLE_DRIVE_CREDENTIALS_PATH', None)
            
            if not credentials_path:
                raise ValueError("GOOGLE_DRIVE_CREDENTIALS_PATH not set in settings")
            
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(f"Google Drive credentials file not found at {credentials_path}")
            
            # Load credentials from JSON file
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=['https://www.googleapis.com/auth/drive']
            )
            
            # Build the Drive service
            self.service = build('drive', 'v3', credentials=credentials)
            
            # Get or create the main folder for uploads
            self.folder_id = self._get_or_create_folder('Activities_Reports')
            
            logger.info("Google Drive service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Drive service: {str(e)}")
            raise
    
    def _get_or_create_folder(self, folder_name):
        """Get existing folder or create new one in the survey shared folder"""
        try:
            # First, try to find the survey shared folder
            survey_folder_id = self._get_shared_folder_id()
            
            if not survey_folder_id:
                raise Exception("Survey shared folder not found. Please ensure the 'survey' folder exists and is shared with the service account.")
            
            # Search for existing folder within the survey folder
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{survey_folder_id}' in parents and trashed=false"
            
            results = self.service.files().list(
                q=query,
                fields="files(id, name)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                return folders[0]['id']
            else:
                # Create new folder within the survey folder
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [survey_folder_id]
                }
                
                folder = self.service.files().create(
                    body=folder_metadata,
                    fields='id',
                    supportsAllDrives=True
                ).execute()
                
                logger.info(f"Created new folder: {folder_name} with ID: {folder.get('id')}")
                return folder.get('id')
                
        except Exception as e:
            logger.error(f"Error getting/creating folder: {str(e)}")
            raise
    
    def _get_shared_folder_id(self):
        """Get the 'survey' shared folder ID from the shared drive"""
        try:
            # First, get the shared drive ID
            shared_drive_id = self._get_shared_drive_id()
            if not shared_drive_id:
                logger.error("No shared drive found. Service account needs access to a shared drive.")
                return None
            
            # Search for the 'survey' folder in the shared drive
            results = self.service.files().list(
                q=f"name='survey' and mimeType='application/vnd.google-apps.folder' and trashed=false",
                fields="files(id, name, parents, driveId)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            folders = results.get('files', [])
            
            # Look for the 'survey' folder in the shared drive
            for folder in folders:
                if folder['name'].lower() == 'survey' and folder.get('driveId') == shared_drive_id:
                    logger.info(f"Found 'survey' folder in shared drive: {folder['name']} (ID: {folder['id']})")
                    return folder['id']
            
            # If not found in shared drive, create it
            logger.info(f"'survey' folder not found in shared drive. Creating it...")
            folder_metadata = {
                'name': 'survey',
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [shared_drive_id]
            }
            
            folder = self.service.files().create(
                body=folder_metadata,
                fields='id',
                supportsAllDrives=True
            ).execute()
            
            logger.info(f"Created 'survey' folder in shared drive with ID: {folder.get('id')}")
            return folder.get('id')
                
        except Exception as e:
            logger.error(f"Error getting shared folder: {str(e)}")
            return None
    
    def _get_shared_drive_id(self):
        """Get the first available shared drive ID"""
        try:
            results = self.service.drives().list(
                fields="drives(id, name)"
            ).execute()
            
            drives = results.get('drives', [])
            if drives:
                logger.info(f"Using shared drive: {drives[0]['name']} (ID: {drives[0]['id']})")
                return drives[0]['id']
            else:
                logger.error("No shared drives found. Service account needs access to a shared drive.")
                return None
                
        except Exception as e:
            logger.error(f"Error getting shared drives: {str(e)}")
            return None
    
    def upload_file(self, file_path, file_name, parent_folder_id=None):
        """
        Upload a file to Google Drive
        
        Args:
            file_path: Local path to the file
            file_name: Name for the file in Google Drive
            parent_folder_id: ID of parent folder (defaults to main folder)
        
        Returns:
            dict: Contains 'file_id', 'web_view_link', 'web_content_link'
        """
        try:
            if not self.service:
                raise Exception("Google Drive service not initialized")
            
            # Use main folder if no parent specified
            if not parent_folder_id:
                parent_folder_id = self.folder_id
            
            # Create activity-specific subfolder
            activity_folder_id = self._get_or_create_activity_folder(file_name, parent_folder_id)
            
            # File metadata
            file_metadata = {
                'name': file_name,
                'parents': [activity_folder_id]
            }
            
            # Upload the file
            media = MediaFileUpload(file_path, resumable=True)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink,webContentLink',
                supportsAllDrives=True
            ).execute()
            
            # Make the file publicly viewable
            self.service.permissions().create(
                fileId=file.get('id'),
                body={'role': 'reader', 'type': 'anyone'},
                supportsAllDrives=True
            ).execute()
            
            # Create a direct view link (without export=download)
            direct_view_link = f"https://drive.google.com/file/d/{file.get('id')}/view"
            
            result = {
                'file_id': file.get('id'),
                'web_view_link': file.get('webViewLink'),
                'web_content_link': direct_view_link,  # Use direct view link instead of download link
                'file_name': file.get('name')
            }
            
            logger.info(f"Successfully uploaded file: {file_name} with ID: {file.get('id')}")
            return result
            
        except Exception as e:
            logger.error(f"Error uploading file {file_name}: {str(e)}")
            raise
    
    def _get_or_create_activity_folder(self, file_name, parent_folder_id):
        """Create a subfolder for each activity based on file name"""
        try:
            # Extract activity identifier from file name (you can modify this logic)
            # For now, we'll create a general "uploads" folder
            folder_name = "uploads"
            
            # Search for existing folder
            results = self.service.files().list(
                q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent_folder_id}' in parents and trashed=false",
                fields="files(id, name)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                return folders[0]['id']
            else:
                # Create new folder
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents': [parent_folder_id]
                }
                
                folder = self.service.files().create(
                    body=folder_metadata,
                    fields='id',
                    supportsAllDrives=True
                ).execute()
                
                return folder.get('id')
                
        except Exception as e:
            logger.error(f"Error creating activity folder: {str(e)}")
            return parent_folder_id  # Fallback to parent folder
    
    def delete_file(self, file_id):
        """Delete a file from Google Drive"""
        try:
            self.service.files().delete(fileId=file_id).execute()
            logger.info(f"Successfully deleted file with ID: {file_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file {file_id}: {str(e)}")
            return False
    
    def get_file_info(self, file_id):
        """Get file information from Google Drive"""
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields='id,name,webViewLink,webContentLink,size,createdTime'
            ).execute()
            
            return {
                'file_id': file.get('id'),
                'name': file.get('name'),
                'web_view_link': file.get('webViewLink'),
                'web_content_link': file.get('webContentLink'),
                'size': file.get('size'),
                'created_time': file.get('createdTime')
            }
        except Exception as e:
            logger.error(f"Error getting file info for {file_id}: {str(e)}")
            return None

# Global instance - lazy initialization
gdrive_service = None

def get_gdrive_service():
    """Get or create the global Google Drive service instance"""
    global gdrive_service
    if gdrive_service is None:
        gdrive_service = GoogleDriveService()
    return gdrive_service
