from django import forms
from emissions import models

class HouseholdForm(forms.ModelForm):
    class Meta:
        model = models.Household
        fields = "__all__"


class TransportationdForm(forms.ModelForm):
    class Meta:
        model = models.Transportation
        fields = "__all__"