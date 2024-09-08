from django import forms
from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm
from django.contrib.auth import get_user_model

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Password'}))

class RegisterForm(BaseUserCreationForm):
    username = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(widget = forms.EmailInput(attrs = {'class':'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Password1'}))
    password2 = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control', 'placeholder': 'Password2'}))
    class Meta:
        model = get_user_model()
        fields = ("username", "email","password1","password2")