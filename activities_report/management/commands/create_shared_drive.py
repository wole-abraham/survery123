from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Create a shared drive for Google Drive integration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--drive-name',
            type=str,
            default='Survey Activities Drive',
            help='Name for the shared drive',
        )

    def handle(self, *args, **options):
        drive_name = options.get('drive_name')
        
        try:
            from activities_report.gdrive_service import get_gdrive_service
            
            gdrive_service = get_gdrive_service()
            
            # Create shared drive
            drive_metadata = {
                'name': drive_name
            }
            
            drive = gdrive_service.service.drives().create(
                body=drive_metadata,
                requestId='unique-request-id-' + str(hash(drive_name))
            ).execute()
            
            self.stdout.write(
                self.style.SUCCESS(f'Shared drive created successfully!')
            )
            self.stdout.write(f'Drive ID: {drive.get("id")}')
            self.stdout.write(f'Drive Name: {drive.get("name")}')
            
        except Exception as e:
            if "already exists" in str(e).lower():
                self.stdout.write(
                    self.style.WARNING('Shared drive already exists or creation failed due to permissions.')
                )
                self.stdout.write('You may need to create a shared drive manually in Google Drive.')
            else:
                raise CommandError(f"Error creating shared drive: {str(e)}")
