from django import forms
from django.contrib.auth.models import User
from .models import File
from django.utils.translation import ugettext_lazy as _


class FileEditForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('title', 'description', 'upload')
        labels = {
            'title': _('Название'),
            'description': _('Описание'),
            'upload': _('Файл')
        }
