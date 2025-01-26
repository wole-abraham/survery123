from rest_framework import serializers
from .models import Activities, ActivityPhoto, ActivityVideo

class ActivityPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityPhoto
        fields = ['id', 'image', 'activity_id']

class ActivityVideoSerializer(serializers.ModelSerializer):
        class Meta:
            model = ActivityVideo
            fields = ['id', 'video', 'activity_id']
    
class ActivitySerializer(serializers.ModelSerializer):
        photos = ActivityPhotoSerializer(many=True, read_only=True)
        videos = ActivityVideoSerializer(many=True, read_only=True)

        class Meta:
              model = Activities
              fields = '__all__'