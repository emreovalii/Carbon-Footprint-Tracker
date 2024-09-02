from django.urls import path
from emissions import views

app_name = "emissions"

urlpatterns = [
    path("household/create",views.HouseholdCreateView.as_view(), name = "household_create") ,
    path("transportation/create",views.TransportationCreateView.as_view(), name = "transportation_create"),
]