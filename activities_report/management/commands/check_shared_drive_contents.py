from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Check contents of the shared drive'

    def handle(self, *args, **options):
        try:
            from activities_report.gdrive_service import get_gdrive_service
            
            gdrive_service = get_gdrive_service()
            
            # Get shared drive ID
            shared_drive_id = gdrive_service._get_shared_drive_id()
            if not shared_drive_id:
                self.stdout.write("No shared drive found!")
                return
            
            self.stdout.write(f"Checking contents of shared drive: {shared_drive_id}")
            
            # List all files and folders in the shared drive
            results = gdrive_service.service.files().list(
                q=f"'{shared_drive_id}' in parents and trashed=false",
                fields="files(id, name, mimeType, parents)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            files = results.get('files', [])
            
            if files:
                self.stdout.write(f"Found {len(files)} items in shared drive:")
                for file in files:
                    file_type = "📁 Folder" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄 File"
                    self.stdout.write(f"  {file_type} - {file['name']} (ID: {file['id']})")
            else:
                self.stdout.write("No files found in shared drive.")
                
        except Exception as e:
            raise CommandError(f"Error checking shared drive contents: {str(e)}")
