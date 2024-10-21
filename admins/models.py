from django.db import models
from django.contrib.auth.models import User

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    employee_id = models.CharField(max_length=20, unique=True)  # Unique ID for admin staff
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    position = models.CharField(max_length=50, blank=True)  # e.g., 'Head Admin', 'Support Admin'
    hire_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.position}"
