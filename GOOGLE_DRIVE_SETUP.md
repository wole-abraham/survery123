# Google Drive Integration Setup

This document explains how to set up Google Drive integration for the Survey Activities application.

## Overview

The application now supports uploading photos and videos directly to Google Drive instead of storing them locally. This provides better scalability, backup, and access to files from anywhere.

## Features

- **Automatic Upload**: Files are automatically uploaded to Google Drive when submitted
- **Fallback Support**: If Google Drive upload fails, files are stored locally as backup
- **Public Access**: Files are made publicly viewable on Google Drive
- **Organized Storage**: Files are organized in folders by activity
- **API Integration**: Full REST API support with Google Drive links

## Setup Instructions

### 1. Create Google Cloud Project and Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Drive API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Drive API"
   - Click "Enable"

### 2. Create Service Account

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the service account details:
   - Name: `survey-activities-drive`
   - Description: `Service account for survey activities file uploads`
4. Click "Create and Continue"
5. Skip the optional steps and click "Done"

### 3. Generate Service Account Key

1. In the Credentials page, find your service account
2. Click on the service account email
3. Go to the "Keys" tab
4. Click "Add Key" > "Create new key"
5. Choose "JSON" format
6. Download the JSON file

### 4. Configure the Application

#### Option A: Using Management Command (Recommended)

```bash
# Copy your credentials file to the project
python manage.py setup_gdrive --credentials-file /path/to/your/credentials.json

# Test the setup
python manage.py setup_gdrive --test-upload
```

#### Option B: Manual Setup

1. Copy your downloaded JSON file to the project root
2. Rename it to `google_drive_credentials.json`
3. Update `survey/settings.py` if needed:
   ```python
   GOOGLE_DRIVE_CREDENTIALS_PATH = '/path/to/your/google_drive_credentials.json'
   GOOGLE_DRIVE_ENABLED = True
   ```

### 5. Install Dependencies

```bash
pip install -r requirements_google_drive.txt
```

### 6. Run Database Migration

```bash
python manage.py makemigrations activities_report
python manage.py migrate
```

## Configuration Options

### Django Settings

Add these settings to your `settings.py`:

```python
# Google Drive Configuration
GOOGLE_DRIVE_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'google_drive_credentials.json')
GOOGLE_DRIVE_ENABLED = True  # Set to False to disable Google Drive integration
```

### Environment Variables (Optional)

You can also use environment variables:

```bash
export GOOGLE_DRIVE_CREDENTIALS_PATH="/path/to/credentials.json"
export GOOGLE_DRIVE_ENABLED="True"
```

## File Structure

Files uploaded to Google Drive are organized as follows:

```
Survey_Activities/
├── uploads/
│   ├── activity_1_photo_image1.jpg
│   ├── activity_1_video_video1.mp4
│   ├── activity_2_photo_image2.png
│   └── ...
```

## API Usage

### Upload Files

Files are automatically uploaded to Google Drive when submitted through the form. The API returns Google Drive links:

```json
{
  "id": 1,
  "activity_id": 1,
  "gdrive_file_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
  "gdrive_web_view_link": "https://drive.google.com/file/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/view",
  "gdrive_web_content_link": "https://drive.google.com/file/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/view",
  "gdrive_file_name": "activity_1_photo_image1.jpg",
  "file_url": "https://drive.google.com/file/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/view",
  "view_url": "https://drive.google.com/file/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/view"
}
```

### Access Files

Use the `file_url` property for viewing files or `view_url` for direct viewing links.

## Troubleshooting

### Common Issues

1. **"Credentials file not found"**
   - Ensure the JSON file is in the correct location
   - Check the file path in settings

2. **"Permission denied"**
   - Verify the service account has Google Drive API access
   - Check that the service account key is valid

3. **"Upload failed"**
   - Check internet connection
   - Verify Google Drive API quota limits
   - Check file size limits (Google Drive has a 5TB limit per file)

### Testing

Use the management command to test your setup:

```bash
python manage.py setup_gdrive --test-upload
```

### Logging

Enable logging to debug issues:

```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'gdrive.log',
        },
    },
    'loggers': {
        'activities_report': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## Security Considerations

1. **Keep credentials secure**: Never commit the JSON credentials file to version control
2. **Use environment variables**: Consider using environment variables for production
3. **Limit permissions**: The service account only needs Google Drive API access
4. **Regular rotation**: Rotate service account keys regularly

## Migration from Local Storage

If you have existing files stored locally, you can migrate them to Google Drive:

1. Keep the existing `image` and `video` fields in the models (they're marked as nullable)
2. Existing files will continue to work through the `file_url` property
3. New uploads will go to Google Drive
4. You can create a migration script to upload existing files to Google Drive

## Support

For issues or questions:
1. Check the logs for error messages
2. Verify your Google Cloud setup
3. Test with the management command
4. Check the Google Drive API documentation
