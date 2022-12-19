from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app_users.models import Profile


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Name')
    phone_number = forms.CharField(required=False, help_text='Phone number')
    city = forms.CharField(max_length=36, required=False, help_text='City')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name']


class VerifyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'is_verified']
