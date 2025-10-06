from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Check contents of the survey folder in shared drive'

    def handle(self, *args, **options):
        try:
            from activities_report.gdrive_service import get_gdrive_service
            
            gdrive_service = get_gdrive_service()
            
            # Get the survey folder ID from shared drive
            survey_folder_id = gdrive_service._get_shared_folder_id()
            if not survey_folder_id:
                self.stdout.write("No survey folder found in shared drive!")
                return
            
            self.stdout.write(f"Checking contents of survey folder: {survey_folder_id}")
            
            # List all files and folders in the survey folder
            results = gdrive_service.service.files().list(
                q=f"'{survey_folder_id}' in parents and trashed=false",
                fields="files(id, name, mimeType, parents, webViewLink)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            files = results.get('files', [])
            
            if files:
                self.stdout.write(f"Found {len(files)} items in survey folder:")
                for file in files:
                    file_type = "📁 Folder" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄 File"
                    self.stdout.write(f"  {file_type} - {file['name']} (ID: {file['id']})")
                    if 'webViewLink' in file:
                        self.stdout.write(f"    View Link: {file['webViewLink']}")
            else:
                self.stdout.write("No files found in survey folder.")
                
        except Exception as e:
            raise CommandError(f"Error checking survey folder contents: {str(e)}")
