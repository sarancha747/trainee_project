from django.db import models
from django.conf import settings


class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="files_created",
                             on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    upload = models.FileField(upload_to=settings.FILE_DIR)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
