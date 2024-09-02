from django.shortcuts import render
from django import views

class HomeView(views.View):
    def get(self,request):
        return render(request,"home/home.html")
