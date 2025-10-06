from django.core.management.base import BaseCommand, CommandError
from activities_report.gdrive_service import get_gdrive_service

class Command(BaseCommand):
    help = 'Check all files in the uploads folder'

    def handle(self, *args, **options):
        try:
            gdrive_service = get_gdrive_service()
            
            # Get the uploads folder ID
            uploads_folder_id = "1eVEbTBw8fpjeAx7N5Bwf1Tr2fQyE0nbf"  # From previous output
            
            self.stdout.write(f"Checking all files in uploads folder: {uploads_folder_id}")
            
            # List all files in the uploads folder
            results = gdrive_service.service.files().list(
                q=f"'{uploads_folder_id}' in parents and trashed=false",
                fields="files(id, name, mimeType, createdTime, size)",
                supportsAllDrives=True,
                includeItemsFromAllDrives=True
            ).execute()
            
            files = results.get('files', [])
            
            if files:
                self.stdout.write(f"Found {len(files)} files in uploads folder:")
                for file in files:
                    file_type = "📁 Folder" if file['mimeType'] == 'application/vnd.google-apps.folder' else "📄 File"
                    size = f" ({file.get('size', 'Unknown')} bytes)" if 'size' in file else ""
                    self.stdout.write(f"  {file_type} - {file['name']}{size}")
                    self.stdout.write(f"    ID: {file['id']}")
                    self.stdout.write(f"    Created: {file.get('createdTime', 'Unknown')}")
                    self.stdout.write("")
            else:
                self.stdout.write("No files found in uploads folder.")
                
        except Exception as e:
            raise CommandError(f"Error checking uploads folder: {str(e)}")
