from rest_framework import serializers
from .models import Activities, ActivityPhoto, ActivityVideo

class ActivityPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityPhoto
        fields = ['id', 'image']
    def to_representation(self, instance):
        # You can manually adjust the image URL if necessary
        data = super().to_representation(instance)
        data['image'] = instance.image.url  # Make sure URL is properly serialized
        return data
    
class ActivityVideoSerializer(serializers.ModelSerializer):
        class Meta:
            model = ActivityVideo
            fields = ['id', 'video']
    
class ActivitySerializer(serializers.ModelSerializer):
        photos = ActivityPhotoSerializer(many=True, read_only=True)
        videos = ActivityVideoSerializer(many=True, read_only=True)

        class Meta:
              model = Activities
              fields = [
            'id', 'project_name', 'date_of_activity', 'planned_activity_category',
            'comment', 'chainage', 'chainage2', 'site_engineer', 'supervisor',
            'party', 'supervision', 'machines', 'machines_source', 'photos', 'videos'
        ]