from django.shortcuts import render
from django.views import generic
from emissions import models

class HouseholdCreateView(generic.CreateView):
    model = models.Household
    fields = "__all__"

class TransportationCreateView(generic.CreateView):
    model = models.Transportation
    fields = "__all__"
    
