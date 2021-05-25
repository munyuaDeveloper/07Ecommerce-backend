from rest_framework import serializers

from fileupload.models import UploadFile


class FileUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
