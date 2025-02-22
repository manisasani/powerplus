from rest_framework import serializers
from .models import Muscle, Exercise

class MuscleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Muscle
        fields = ['id', 'name', 'image', 'description', 'create_at']

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class ExerciseSerializer(serializers.ModelSerializer):
    muscle_detail = MuscleSerializer(source='muscle', read_only=True)
    
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'muscle', 'muscle_detail', 'video', 'description', 'tags', 'create_at']

    def get_video_url(self, obj):
        if obj.video:
            return self.context['request'].build_absolute_uri(obj.video.url)
        return None