from rest_framework import serializers
from .models import Activities, ActivityPhoto, ActivityVideo

class ActivityPhotoSerializer(serializers.ModelSerializer):
    # Override the image field to return the file URL
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = ActivityPhoto
        fields = ['id', 'image', 'activity_id']
    
    def get_image(self, obj):
        """Return the file URL (Google Drive or local)"""
        return obj.file_url

class ActivityVideoSerializer(serializers.ModelSerializer):
    # Override the video field to return the file URL
    video = serializers.SerializerMethodField()
    
    class Meta:
        model = ActivityVideo
        fields = ['id', 'video', 'activity_id']
    
    def get_video(self, obj):
        """Return the file URL (Google Drive or local)"""
        return obj.file_url
    
class ActivitySerializer(serializers.ModelSerializer):
    photos = ActivityPhotoSerializer(many=True, read_only=True)
    videos = ActivityVideoSerializer(many=True, read_only=True)

    class Meta:
        model = Activities
        fields = '__all__'