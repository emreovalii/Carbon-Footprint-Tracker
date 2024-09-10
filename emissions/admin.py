from django.contrib import admin
from emissions import models

@admin.register(models.Household)
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ("id","user","consumption_type","consumption_value","month_period","created_at")
    list_filter = ("created_at",)
    search_fields = ("user__first_name", "user__last_name")
    search_help_text = " user first name and user last name."
    autocomplete_fields = ("user",)


@admin.register (models.Transportation)
class TransportationAdmin(admin.ModelAdmin):
    list_display = ("id","user","vehicle_type","distance","is_public","transportation_date","created_at")
    search_fields = ("user__first_name", "user__last_name")
    search_help_text = " user first name and user last name."
    autocomplete_fields = ("user",)
