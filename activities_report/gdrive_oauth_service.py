import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDriveOAuthService:
    def __init__(self):
        self.service = None
        self.folder_id = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Drive service with OAuth credentials"""
        try:
            creds = None
            # The file token.json stores the user's access and refresh tokens.
            token_path = os.path.join(settings.BASE_DIR, 'token.json')
            credentials_path = getattr(settings, 'GOOGLE_DRIVE_CREDENTIALS_PATH', None)
            
            if not credentials_path:
                raise ValueError("GOOGLE_DRIVE_CREDENTIALS_PATH not set in settings")
            
            if not os.path.exists(credentials_path):
                raise FileNotFoundError(f"Google Drive credentials file not found at {credentials_path}")
            
            if os.path.exists(token_path):
                creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())
            
            # Build the Drive service
            self.service = build('drive', 'v3', credentials=creds)
            
            # Get or create the main folder for uploads
            self.folder_id = self._get_or_create_folder('Survey_Activities')
            
            logger.info("Google Drive OAuth service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Drive OAuth service: {str(e)}")
            raise
    
    def _get_or_create_folder(self, folder_name):
        """Get existing folder or create new one"""
        try:
            # Search for existing folder
            results = self.service.files().list(
                q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
                fields="files(id, name)"
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                return folders[0]['id']
            else:
                # Create new folder
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                
                folder = self.service.files().create(
                    body=folder_metadata,
                    fields='id'
                ).execute()
                
                logger.info(f"Created new folder: {folder_name} with ID: {folder.get('id')}")
                return folder.get('id')
                
        except Exception as e:
            logger.error(f"Error getting/creating folder: {str(e)}")
            raise
    
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
                fields='id,name,webViewLink,webContentLink'
            ).execute()
            
            # Make the file publicly viewable
            self.service.permissions().create(
                fileId=file.get('id'),
                body={'role': 'reader', 'type': 'anyone'}
            ).execute()
            
            # Create a direct view link (without export=download)
            direct_view_link = f"https://drive.google.com/file/d/{file.get('id')}/view"
            
            result = {
                'file_id': file.get('id'),
                'web_view_link': file.get('webViewLink'),
                'web_content_link': direct_view_link,
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
                fields="files(id, name)"
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
                    fields='id'
                ).execute()
                
                return folder.get('id')
                
        except Exception as e:
            logger.error(f"Error creating activity folder: {str(e)}")
            return parent_folder_id  # Fallback to parent folder
