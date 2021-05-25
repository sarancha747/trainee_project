from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User, auth
from .forms import FileEditForm
from django.conf import settings
import filecmp
import os


@login_required(login_url='login')
def repository(request):
    user = auth.get_user(request)
    files = user.files_created.all()
    if request.method == 'POST':
        form = FileEditForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file_response_code = check_uploaded_file(file.upload.name.replace(" ", "_"), file.upload)
            file.user = request.user
            if file_response_code == 1:
                file.save()
            if file_response_code == 2:
                file.upload = settings.FILE_DIR + file.upload.name
                file.save()
            if file_response_code == 3:
                file.save()
    else:
        form = FileEditForm
    return render(request, 'repository/repository.html', {'files': files, 'form': form})


def check_uploaded_file(file_name, file_to_save):
    """
    1 - файл с даним название не найден
    2 - файл с даним название найден, наполнение соотвествует
    3 - файл с даним название найден, нонаполнение не соотвествует
    """
    main_file_dir = os.path.join(os.path.dirname(settings.PROJECT_DIR), settings.FILE_DIR)
    temp_file_dir = os.path.join(os.path.dirname(settings.PROJECT_DIR), settings.TEMP_FILE_DIR)
    if file_name in os.listdir(main_file_dir):
        # Проверяем вариант когда два пользователя добавил файл с одинаковым именем, но с разным наполнением
        with open(os.path.join(temp_file_dir, file_name), 'wb+') as destination:
            for chunk in file_to_save.chunks():
                destination.write(chunk)
        common = [file_name]
        match, mismatch, errors = filecmp.cmpfiles(main_file_dir, temp_file_dir, common, shallow=False)
        if file_name in match:
            # Файл найден, но наполнение соотвествует. Не сохранять файл
            file_response_code = 2
        else:
            # Файл найден, нонаполнение не соотвествует. Сохранить файл
            file_response_code = 3
        os.remove(os.path.join(temp_file_dir, file_name))
    else:
        # Файл не найден. Сохранить файл
        file_response_code = 1
    return file_response_code
