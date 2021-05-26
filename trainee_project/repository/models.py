from django.db import models
from django.conf import settings


class FileHash(models.Model):
    file_hash = models.CharField(max_length=256, unique=True)
    real_file = models.FileField(upload_to=settings.FILE_DIR)

    def __str__(self):
        return self.real_file.name


class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="files_created",
                             on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user_file_title = models.CharField(max_length=200)
    upload = models.ForeignKey(FileHash, on_delete=models.CASCADE, null=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
