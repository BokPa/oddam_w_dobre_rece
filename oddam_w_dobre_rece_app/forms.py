from django.utils import timezone

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):

    name = forms.CharField(max_length=64)
    surname = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean(self):
        cd = super().clean()
        pass1 = cd.get('password')
        pass2 = cd.get('password2')
        username = cd.get('email')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Nazwa użytkownika jest zajęta.")
        if pass1 != pass2:
            raise ValidationError("Podaj poprawnie obydwa hasła.")

        return cd

