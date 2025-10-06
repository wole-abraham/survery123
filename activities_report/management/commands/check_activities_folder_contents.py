from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Check contents of the Activities_Reports folder'

    def handle(self, *args, **options):
        try:
            from activities_report.gdrive_service import get_gdrive_service
            
            gdrive_service = get_gdrive_service()
            
            # Get the Activities_Reports folder ID
            activities_folder_id = "15l28c6IJkFIXLolAAZplvwx32jlQBgcH"  # From previous output
            
            self.stdout.write(f"Checking contents of Activities_Reports folder: {activities_folder_id}")
            
            # List all files and folders in the Activities_Reports folder
            results = gdrive_service.service.files().list(
                q=f"'{activities_folder_id}' in parents and trashed=false",
                fields="files(id, name, mimeType, parents, webViewLink, createdTime)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            files = results.get('files', [])
            
            if files:
                self.stdout.write(f"Found {len(files)} items in Activities_Reports folder:")
                for file in files:
                    file_type = "📁 Folder" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄 File"
                    self.stdout.write(f"  {file_type} - {file['name']} (ID: {file['id']})")
                    if 'webViewLink' in file:
                        self.stdout.write(f"    View Link: {file['webViewLink']}")
                    if 'createdTime' in file:
                        self.stdout.write(f"    Created: {file['createdTime']}")
            else:
                self.stdout.write("No files found in Activities_Reports folder.")
                
        except Exception as e:
            raise CommandError(f"Error checking Activities_Reports folder contents: {str(e)}")
