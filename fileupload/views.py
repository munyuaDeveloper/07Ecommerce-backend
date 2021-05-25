from rest_framework import generics, permissions, status
from rest_framework.response import Response

from fileupload.models import UploadFile
from fileupload.serializers import FileUploadSerializer

import os


class UploadFileView(generics.CreateAPIView):
    queryset = UploadFile.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request):
        images = request.FILES.getlist("image")
        all_images = []
        for image in images:
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
            all_images.append(image_inst.id)

        return Response(all_images)


class FileDetailsView(generics.ListAPIView):
    queryset = UploadFile.objects.all()
    serializer_class = FileUploadSerializer

    def get_queryset(self):
        payload = self.request.query_params.dict()
        images = payload['image'].split(',')
        image_instance = UploadFile.objects.filter(
            id__in=images).order_by('id')
        return image_instance
