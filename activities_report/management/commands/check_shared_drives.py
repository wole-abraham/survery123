from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Check if the service account can access the survey shared folder'

    def handle(self, *args, **options):
        try:
            from activities_report.gdrive_service import get_gdrive_service
            
            gdrive_service = get_gdrive_service()
            
            # Search for the 'survey' folder
            results = gdrive_service.service.files().list(
                q="name='survey' and mimeType='application/vnd.google-apps.folder' and trashed=false",
                fields="files(id, name, parents)"
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                self.stdout.write(
                    self.style.SUCCESS(f'Found {len(folders)} folder(s) named "survey":')
                )
                for folder in folders:
                    self.stdout.write(f"  - Name: {folder['name']}")
                    self.stdout.write(f"    ID: {folder['id']}")
                    if 'parents' in folder:
                        self.stdout.write(f"    Parent ID: {folder['parents'][0] if folder['parents'] else 'Root'}")
                    self.stdout.write("")
                
                # Test if we can create a folder inside the survey folder
                try:
                    survey_folder_id = folders[0]['id']
                    test_folder_metadata = {
                        'name': 'test_folder_permissions',
                        'mimeType': 'application/vnd.google-apps.folder',
                        'parents': [survey_folder_id]
                    }
                    
                    test_folder = gdrive_service.service.files().create(
                        body=test_folder_metadata,
                        fields='id'
                    ).execute()
                    
                    # Clean up test folder
                    gdrive_service.service.files().delete(fileId=test_folder['id']).execute()
                    
                    self.stdout.write(
                        self.style.SUCCESS('✅ Service account has write access to the survey folder!')
                    )
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'❌ Service account does not have write access: {str(e)}')
                    )
                    self.stdout.write("")
                    self.stdout.write("To fix this:")
                    self.stdout.write("1. Go to Google Drive in your browser")
                    self.stdout.write("2. Find the 'survey' folder")
                    self.stdout.write("3. Right-click on it and select 'Share'")
                    self.stdout.write("4. Add your service account email")
                    self.stdout.write("5. Give it 'Editor' or 'Manager' role")
                    
            else:
                self.stdout.write(
                    self.style.ERROR('No "survey" folder found!')
                )
                self.stdout.write("")
                self.stdout.write("To fix this:")
                self.stdout.write("1. Create a folder named 'survey' in Google Drive")
                self.stdout.write("2. Right-click on it and select 'Share'")
                self.stdout.write("3. Add your service account email")
                self.stdout.write("4. Give it 'Editor' or 'Manager' role")
                self.stdout.write("")
                
            # Show service account email
            try:
                credentials_path = getattr(settings, 'GOOGLE_DRIVE_CREDENTIALS_PATH', None)
                if credentials_path and os.path.exists(credentials_path):
                    import json
                    with open(credentials_path, 'r') as f:
                        creds = json.load(f)
                        if 'client_email' in creds:
                            self.stdout.write(f"Service account email: {creds['client_email']}")
            except Exception as e:
                self.stdout.write(f"Could not read service account email: {str(e)}")
                
        except Exception as e:
            raise CommandError(f"Error checking shared folder: {str(e)}")
