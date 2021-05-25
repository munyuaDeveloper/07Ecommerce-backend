from fileupload.views import UploadFileView
from django.conf.urls import url


urlpatterns = [
    url('upload-image', UploadFileView.as_view(), name='upload-image'),
]
