from django import views
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from accounts import forms
from django.contrib.auth import login,authenticate


class CustomLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "accounts/login.html"

class RegisterView(views.View):

    def get(self, request):
        form = forms.RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(self.request, 'User registration successful')
            return redirect('/')
        return render(request, 'accounts/register.html', {'form': form})

class CustomLogoutView(LogoutView):
    template_name = "accounts/logout.html"