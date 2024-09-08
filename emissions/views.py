from django.shortcuts import render
from django.views import generic
from emissions import models,forms
from django.http import HttpResponseRedirect

class HouseholdCreateView(generic.CreateView):
    model = models.Household
    form_class = forms.HouseholdForm

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TransportationCreateView(generic.CreateView):
    model = models.Transportation
    form_class = forms.TransportationForm

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
