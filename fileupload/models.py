from django.db import models

# Create your models here.


class UploadFile(models.Model):
    image = models.ImageField(upload_to='product_images/')
    uploaded_by = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
