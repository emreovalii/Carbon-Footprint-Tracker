from django.contrib import admin
from accounts import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("username",)