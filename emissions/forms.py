from django import forms
from emissions import models

class HouseholdForm(forms.ModelForm):
    consumption_type = forms.ChoiceField(widget = forms.Select(attrs = {'class':'form-control', 'placeholder': '---'}),choices = models.CONSUMPTION_TYPE_CHOICES)
    consumption_value = forms.FloatField(widget = forms.NumberInput(attrs = {'class':'form-control', 'placeholder': '0.0'}))
    month_period = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control', 'placeholder': 'yyyy-mm'}))
    class Meta:
        model = models.Household
        exclude = ("user",)


class TransportationForm(forms.ModelForm):
    vehicle_type = forms.ChoiceField(widget = forms.Select(attrs = {'class':'form-control', 'placeholder': '---'}),choices = models.VEHICLE_TYPE_CHOICES)
    distance = forms.FloatField(widget = forms.NumberInput(attrs = {'class':'form-control', 'placeholder': 'Km'}))
    is_public = forms.BooleanField(required = False)
    
    class Meta:
        model = models.Transportation
        exclude = ("user",)