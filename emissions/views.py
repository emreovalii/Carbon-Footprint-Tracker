from django.shortcuts import render
from django.views import generic,View
from emissions import models,forms
from django.http import HttpResponseRedirect
from django.db.models import Sum,Case,When,F,FloatField
from decouple import config


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

class EmissionReportView(View):

    def get(self, request):
       context = {}

       # Transportation verilerini grupla ve topla (gün bazlı)
       transportation_queryset = models.Transportation.objects.filter(user=request.user)

       total_emission_transportation_by_date = list(transportation_queryset.annotate(
           per_emission=Case(
               When(vehicle_type="car", then=F("distance") * float(config("CAR_EMISSION"))),
               When(vehicle_type="bus", then=F("distance") * float(config("BUS_EMISSION"))),
               When(vehicle_type="plane", then=F("distance") * float(config("PLANE_EMISSION"))),
               When(vehicle_type="subway", then=F("distance") * float(config("SUBWAY_EMISSION"))),
               When(vehicle_type="walking", then=F("distance") * 0),
               When(vehicle_type="cycling", then=F("distance") * 0),
               output_field=FloatField()
           )
       ).values("transportation_date").annotate(
           total_emission=Sum("per_emission")  # per_emission'ı topluyoruz
       ))

       # Household verilerini grupla ve topla (gün bazlı veya aylık bazda)
       household_queryset = models.Household.objects.filter(user=request.user)
       total_emission_household_by_month = list(household_queryset.annotate(
           per_emission=Case(
               When(consumption_type="electricity", then=F("consumption_value") * float(config("ELECTRICITY_EMISSION"))),
               When(consumption_type="water", then=F("consumption_value") * float(config("WATER_EMISSION"))),
               When(consumption_type="heating", then=F("consumption_value") * float(config("HEATING_EMISSION"))),
               output_field=FloatField()
           )
       ).values("month_period").annotate(
           total_emission=Sum("per_emission")  # per_emission'ı topluyoruz
       ))

       context["transportation_by_date"] = total_emission_transportation_by_date
       context["household_by_month"] = total_emission_household_by_month
       
       return render(request, "reports/reports.html", context)
      