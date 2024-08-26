from django.utils import timezone

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

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

class UserUpdateForm(forms.ModelForm):
    current_password = forms.CharField(label="Aktualne hasło", widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.instance.check_password(current_password):
            raise forms.ValidationError("Aktualne hasło jest nieprawidłowe.")
        return current_password


class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = forms.CharField(label="Stare hasło", widget=forms.PasswordInput)
    new_password1 = forms.CharField(label="Nowe hasło", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Powtórz nowe hasło", widget=forms.PasswordInput)

    class Meta:
        fields = ('old_password', 'new_password1', 'new_password2')