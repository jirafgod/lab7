from django import forms
from django.contrib.auth.models import User
from django.db import models


class Events(models.Model):
    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
    name = models.CharField(max_length=15)
    city = models.IntegerField()


class RegisterForm(forms.Form):
    login = forms.CharField(label='Логин', min_length=5)
    password = forms.CharField(label='Пароль', min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Пароль 2', min_length=8, widget=forms.PasswordInput)
    email = forms.CharField(label='E-mail', min_length=1)
    last_name = forms.CharField(label='Фамилия', min_length=1)
    first_name = forms.CharField(label='Имя', min_length=1)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Пароли не совпадают")
        usrs = User.objects.filter(username=cleaned_data.get('login'))
        if len(usrs) > 0:
            raise forms.ValidationError("Логин занят")


class LoginForm(forms.Form):
    login = forms.CharField(label='Логин', min_length=5)
    password = forms.CharField(label='Пароль', min_length=8, widget=forms.PasswordInput)
