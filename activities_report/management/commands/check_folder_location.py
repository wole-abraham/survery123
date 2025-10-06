from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Check if the survey folder is in a shared drive or personal drive'

    def handle(self, *args, **options):
        try:
            from activities_report.gdrive_service import get_gdrive_service
            
            gdrive_service = get_gdrive_service()
            
            # Get the survey folder details
            results = gdrive_service.service.files().list(
                q="name='survey' and mimeType='application/vnd.google-apps.folder' and trashed=false",
                fields="files(id, name, parents, driveId)"
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                folder = folders[0]
                self.stdout.write(f"Survey folder details:")
                self.stdout.write(f"  - Name: {folder['name']}")
                self.stdout.write(f"  - ID: {folder['id']}")
                
                if 'driveId' in folder:
                    self.stdout.write(f"  - Drive ID: {folder['driveId']}")
                    self.stdout.write("  ✅ This folder is in a shared drive!")
                else:
                    self.stdout.write("  ❌ This folder is in a personal drive (not a shared drive)")
                    self.stdout.write("")
                    self.stdout.write("SOLUTION:")
                    self.stdout.write("1. Create a shared drive in Google Drive")
                    self.stdout.write("2. Move the 'survey' folder into the shared drive")
                    self.stdout.write("3. Or create a new 'survey' folder inside the shared drive")
                    self.stdout.write("")
                    self.stdout.write("To create a shared drive:")
                    self.stdout.write("1. Go to Google Drive")
                    self.stdout.write("2. Click 'New' > 'Shared drive'")
                    self.stdout.write("3. Name it 'Survey Drive' or similar")
                    self.stdout.write("4. Add your service account as a member with 'Manager' role")
                
                if 'parents' in folder:
                    parent_id = folder['parents'][0] if folder['parents'] else 'Root'
                    self.stdout.write(f"  - Parent ID: {parent_id}")
                    
            else:
                self.stdout.write("No survey folder found!")
                
        except Exception as e:
            raise CommandError(f"Error checking folder location: {str(e)}")
