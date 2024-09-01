import uuid
from django.db import models
from django.contrib.auth import get_user_model

class Household(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    heating = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    electricity = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    water = models.DecimalField(max_digits = 6, decimal_places = 2, default = 0)
    month_period = models.CharField(max_length = 50, help_text = "yyyy-mm")
    user = models.ForeignKey(get_user_model(), on_delete = models.CASCADE)
    created_at = models.DateField(auto_now_add = True)


