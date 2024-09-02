from django import forms
from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm
from django.contrib.auth import get_user_model

class LoginForm(AuthenticationForm):
    pass

class RegisterForm(BaseUserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email","password1","password2")