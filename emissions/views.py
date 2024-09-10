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

    def get(self,request):
        context = {}
        transportation_queryset = models.Transportation.objects.filter(user = request.user)
        total_emission_transportation = transportation_queryset.annotate(
            per_emission = Case(
                When(vehicle_type = "car",then = F("distance")* float(config("CAR_EMISSION"))),
                When(vehicle_type = "bus",then = F("distance")* float(config("BUS_EMISSION"))),
                When(vehicle_type = "plane",then = F("distance")* float(config("PLANE_EMISSION"))),
                When(vehicle_type = "subway",then = F("distance")* float(config("SUBWAY_EMISSION"))),
                When(vehicle_type = "walking",then = F("distance")* 0),
                When(vehicle_type = "cycling",then = F("distance")* 0),
                output_field = FloatField()

            )
        ).aggregate(total_emission = Sum("per_emission"))
        
        context["transportations"] = transportation_queryset
        context["total_emission_transportation"] = total_emission_transportation["total_emission"]
        

        return render(request,"reports/reports.html",context)

