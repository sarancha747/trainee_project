from rest_framework import serializers

from .models import File


class UploadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=2000)
    upload = serializers.FileField()


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'user', 'title', 'description', 'user_file_title', 'upload', 'created']
