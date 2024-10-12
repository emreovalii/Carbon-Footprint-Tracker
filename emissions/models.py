import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from decouple import config

VEHICLE_TYPE_CHOICES = (
        ("car","Car"),
        ("walking","Walking"),
        ("subway","Subway"),
        ("cycling","Cycling"),
        ("bus","Bus"),
        ("plane","Plane")
    )

CONSUMPTION_TYPE_CHOICES = (
        ("heating","Heating"),
        ("electricity","Electricity"),
        ("water","Water"),
    )
class Household(models.Model):


    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    
    
    consumption_type = models.CharField(max_length = 50, choices = CONSUMPTION_TYPE_CHOICES)
    consumption_value = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    month_period = models.CharField(max_length = 50, help_text = "yyyy-mm")
    user = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    created_at = models.DateField(auto_now_add = True)
    
    
    def get_absolute_url(self):
        return reverse("home")


    class Meta:
        unique_together = ("consumption_type","month_period","user")


    @property
    def get_sum_emissions(self):
        #TODO : household modeline göre düzenlenmesi gerekiyor
        if self.consumption_type == "electricity":
            return float(self.consumption_value) * float(config("ELECTRICITY_EMISSION"))
        elif self.consumption_type == "water":
            return float(self.consumption_value) * float(config("WATER_EMISSION"))
        elif self.consumption_type == "heating":
            return float(self.consumption_value) * float(config("HEATING_EMISSION"))
        


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



    
    
    @property
    def get_sum_emissions(self):
        
        if self.vehicle_type == "car":
            return self.distance * float(config("CAR_EMISSION"))
        elif self.vehicle_type == "walking":
            return self.distance * 0
        elif self.vehicle_type == "subway":
            return self.distance * float(config("SUBWAY_EMISSION"))
        elif self.vehicle_type == "cycling":
            return self.distance * 0
        elif self.vehicle_type == "bus":
            return self.distance * float(config("BUS_EMISSION"))
        elif self.vehicle_type == "plane":
            return self.distance * float(config("PLANE_EMISSION"))


    

    

