from fileupload.views import UploadFileView, FileDetailsView
from django.conf.urls import url


urlpatterns = [
    url('upload-image', UploadFileView.as_view(), name='upload-image'),
    url('list-image', FileDetailsView.as_view(), name='list-image'),
]
