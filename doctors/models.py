from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    schedule = models.TextField()  # JSON for schedule

    def __str__(self):
        return f"{self.user.username} ({self.specialty})"

