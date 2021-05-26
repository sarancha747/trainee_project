from django.contrib import admin
from .models import File, FileHash

admin.site.register(File)
admin.site.register(FileHash)
# Register your models here.
