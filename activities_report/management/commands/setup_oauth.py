from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Setup Google Drive OAuth integration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--credentials-file',
            type=str,
            help='Path to Google Drive OAuth credentials JSON file',
        )
        parser.add_argument(
            '--test-upload',
            action='store_true',
            help='Test Google Drive upload functionality',
        )

    def handle(self, *args, **options):
        credentials_file = options.get('credentials_file')
        
        if credentials_file:
            self.setup_credentials(credentials_file)
        
        if options.get('test_upload'):
            self.test_upload()
        
        self.stdout.write(
            self.style.SUCCESS('Google Drive OAuth setup completed successfully!')
        )

    def setup_credentials(self, credentials_file):
        """Copy credentials file to the project root"""
        try:
            if not os.path.exists(credentials_file):
                raise CommandError(f"Credentials file not found: {credentials_file}")
            
            # Copy to project root
            target_path = os.path.join(settings.BASE_DIR, 'google_drive_credentials.json')
            
            with open(credentials_file, 'r') as source:
                with open(target_path, 'w') as target:
                    target.write(source.read())
            
            self.stdout.write(
                self.style.SUCCESS(f'OAuth credentials file copied to: {target_path}')
            )
            self.stdout.write(
                self.style.WARNING('Next time you run the app, it will open a browser for OAuth authorization.')
            )
            
        except Exception as e:
            raise CommandError(f"Error setting up credentials: {str(e)}")

    def test_upload(self):
        """Test Google Drive upload functionality"""
        try:
            from activities_report.gdrive_oauth_service import GoogleDriveOAuthService
            
            # Create service instance
            gdrive_service = GoogleDriveOAuthService()
            
            # Create a test file
            test_file_path = os.path.join(settings.BASE_DIR, 'test_upload.txt')
            with open(test_file_path, 'w') as f:
                f.write("This is a test file for Google Drive OAuth integration.")
            
            # Upload test file
            result = gdrive_service.upload_file(
                file_path=test_file_path,
                file_name="test_upload.txt"
            )
            
            if result:
                self.stdout.write(
                    self.style.SUCCESS(f'Test upload successful! File ID: {result["file_id"]}')
                )
                self.stdout.write(f'Web View Link: {result["web_view_link"]}')
                
                # Clean up test file
                os.unlink(test_file_path)
                
                self.stdout.write("Test file cleaned up locally.")
            else:
                raise CommandError("Test upload failed")
                
        except Exception as e:
            raise CommandError(f"Test upload failed: {str(e)}")
