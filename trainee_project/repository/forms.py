from django import forms
from django.contrib.auth.models import User
from .models import File
from django.utils.translation import ugettext_lazy as _


class FileEditForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(max_length=2000, widget=forms.Textarea)
    upload = forms.FileField()