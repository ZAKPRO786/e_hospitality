# admin.py for doctors app

from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'license_number')
    search_fields = ('user__username', 'specialty', 'license_number')
    list_filter = ('specialty',)
    ordering = ('user__username',)
from django.contrib import admin

# Register your models here.
