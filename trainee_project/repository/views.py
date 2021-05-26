from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User, auth
from .models import File, FileHash
from .forms import FileEditForm
from django.conf import settings
import filecmp
import os
import hashlib


@login_required(login_url='login')
def repository(request):
    user = auth.get_user(request)
    files = user.files_created.all()
    if request.method == 'POST':
        form = FileEditForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            upload = form.cleaned_data['upload']
            real_file_id = check_uploaded_file_hash(upload)
            File.objects.create(user=user, title=title, description=description,
                                user_file_title=upload.name, upload=real_file_id)
    else:
        form = FileEditForm
    return render(request, 'repository/repository.html', {'files': files, 'form': form})


def check_uploaded_file_hash(file_to_save):
    file_hash = hashlib.sha256()
    for chunk in file_to_save.chunks():
        file_hash.update(chunk)
    if file_hash.hexdigest() in FileHash.objects.values_list('file_hash',
                                                             flat=True).filter(file_hash=file_hash.hexdigest()):
        # Хеш есть в базе, возвращаем объект записи в базе
        return FileHash.objects.get(file_hash=file_hash.hexdigest())
    else:
        # Хеша нет в базе, создаём запись и возвращаем её
        return FileHash.objects.create(file_hash=file_hash.hexdigest(), real_file=file_to_save)
