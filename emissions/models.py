import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

VEHICLE_TYPE_CHOICES = (
        ("car","Car"),
        ("walking","Walking"),
        ("subway","Subway"),
        ("cycling","Cycling"),
        ("bus","Bus"),
        ("plane","Plane")
    )

class Household(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    heating = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    electricity = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    water = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    month_period = models.CharField(max_length = 50, help_text = "yyyy-mm")
    user = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    created_at = models.DateField(auto_now_add = True)
    
    def get_absolute_url(self):
        return reverse("home")


class Transportation(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    
    vehicle_type = models.CharField(max_length = 50, help_text = "Type Of vehicle", choices = VEHICLE_TYPE_CHOICES )
    distance = models.PositiveSmallIntegerField()
    is_public = models.BooleanField(default = False)
    transportation_date = models.DateField(auto_now_add = True)
    created_at = models.DateField(auto_now_add = True)
    user = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)

    def get_absolute_url(self):
        return reverse("home")

