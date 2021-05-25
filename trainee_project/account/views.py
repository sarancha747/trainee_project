from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Create your views here.
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        if password == password_confirmation and password != "":
            if User.objects.filter(username=username).exists() or username == "":
                messages.info(request, "Юзернейм занят")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Данный Email уже зарегестрирован")
                return redirect("register")
            elif not val_email(email):
                messages.info(request, "Невалидный Email ")
                return redirect("register")
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=username,
                                                last_name=username)
                user.save();
                return redirect("login")
        else:
            messages.info(request, "Пароли не совпадают")
            return redirect("register")
    else:
        return render(request, "registration/registration.html")


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Введён неверный пароль или юзернейм")
            return redirect("login")
    else:
        return render(request, "login/login.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


def val_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
