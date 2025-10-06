from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'List all shared drives the service account can access'

    def handle(self, *args, **options):
        try:
            from activities_report.gdrive_service import get_gdrive_service
            
            gdrive_service = get_gdrive_service()
            
            # List all shared drives
            results = gdrive_service.service.drives().list(
                fields="drives(id, name, capabilities)"
            ).execute()
            
            drives = results.get('drives', [])
            
            if drives:
                self.stdout.write(
                    self.style.SUCCESS(f'Found {len(drives)} shared drive(s):')
                )
                for drive in drives:
                    self.stdout.write(f"  - Name: {drive['name']}")
                    self.stdout.write(f"    ID: {drive['id']}")
                    if 'capabilities' in drive:
                        caps = drive['capabilities']
                        self.stdout.write(f"    Can create files: {caps.get('canCreateFiles', 'Unknown')}")
                        self.stdout.write(f"    Can create folders: {caps.get('canCreateFolders', 'Unknown')}")
                    self.stdout.write("")
            else:
                self.stdout.write(
                    self.style.ERROR('No shared drives found!')
                )
                self.stdout.write("")
                self.stdout.write("Make sure you:")
                self.stdout.write("1. Created a shared drive in Google Drive")
                self.stdout.write("2. Added the service account as a member")
                self.stdout.write("3. Gave it 'Manager' or 'Content manager' role")
                self.stdout.write("")
                self.stdout.write(f"Service account email: survey-upload@surveyapp-474300.iam.gserviceaccount.com")
                
        except Exception as e:
            raise CommandError(f"Error listing shared drives: {str(e)}")
