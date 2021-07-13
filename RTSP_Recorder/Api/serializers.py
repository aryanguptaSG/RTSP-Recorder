from rest_framework import serializers
from .models import Recording,Camera

'''This is serilizer for camera class'''
class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ['name','url','status','active_hours']


''' This is serilizer for recording class'''
class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = ['name','path','status','datetime']
    