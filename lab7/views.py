from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.views import View
from django.contrib.auth.decorators import login_required

from lab7.models import *


@login_required(login_url='/login')
def index(request):
    a = 'You are authenticated'
    return render(request, 'index.html', {'auth': a})


def index2(request):
    a = 'You are authenticated'
    if request.user.is_authenticated():
        return render(request, 'index.html', {'auth': a})
    else:
        return redirect('/login')


def log(request):
    logout(request)
    return redirect('/')


class reg1(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        errors = []
        login = request.POST.get('login', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        last_name = request.POST.get('last_name', '')
        first_name = request.POST.get('first_name', '')

        if len(login) < 5:
            errors.append("Логин короткий")
        if len(password) < 8:
            errors.append("Пароль короткий")
        if password != password2:
            errors.append("Пароли не совпадают")
        if not len(email) or not len(last_name) or not len(first_name):
            errors.append("Все поля должны быть заполнены")

        if len(errors) == 0:
            usrs = User.objects.filter(username=login)
            if len(usrs) > 0:
                errors.append("Пользователь с данным логином уже существует")
            else:
                u = User(username=login, email=email, last_name=last_name, first_name=first_name)
                u.set_password(password)
                u.save()

        if len(errors) > 0:
            return render(request, 'register.html', {'errors': errors, 'login': login,
                                                     'email': email, 'last_name': last_name, 'first_name': first_name})
        return redirect('/login', {'errors': 'Вы зарегестрировались, авторизируйтесь.'})


class reg2(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register2.html', {'errors': '', 'form': form.as_p()})

    def post(self, request):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return render(request, 'register2.html', {'errors': '', 'form': form.as_p()})

        u = User(username=form.cleaned_data['login'], email=form.cleaned_data['email'],
                 last_name=form.cleaned_data['last_name'], first_name=form.cleaned_data['first_name'])
        u.set_password(form.cleaned_data['password'])
        u.save()
        return redirect('/login', {'errors': 'Вы зарегестрировались, авторизируйтесь.'})


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        log = request.POST.get('login', '')
        password = request.POST.get('password', '')
        errors = []

        user = authenticate(username=log, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        errors.append('Логин или пароль неверны')
        return render(request, 'login.html', {'errors': errors, 'login': login})
