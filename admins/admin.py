# admin/admin.py
from django.contrib import admin
from .models import Admin

class CustomAdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'position', 'hire_date')
    search_fields = ('user__username', 'employee_id', 'position')

admin.site.register(Admin, CustomAdminAdmin)
