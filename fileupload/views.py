from rest_framework import generics, permissions, status
from rest_framework.response import Response

from fileupload.models import UploadFile
from fileupload.serializers import FileUploadSerializer

import os


class UploadFileView(generics.CreateAPIView):
    queryset = UploadFile.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        image = request.FILES.get("image")
        if image.size > 15360 * 1024:
            return Response(
                {'details': 'File is too large'},
                status=status.HTTP_400_BAD_REQUEST)

        allowed_extension = ['.jpeg', '.jpg', '.png', ]
        extension = os.path.splitext(image.name)[1]
        if extension not in allowed_extension:
            return Response(
                {"details": "Invalid image"},
                status=status.HTTP_400_BAD_REQUEST)
        image_param = {
            "image": image
        }
        image_inst = UploadFile.objects.create(**image_param)
        return Response({"id": image_inst.id})
