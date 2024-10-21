# models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient_id = models.CharField(max_length=20, unique=True)
    patient_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    height = models.DecimalField(max_digits=4, decimal_places=2)  # in feet
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # in kilograms
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    registration_date = models.DateField(auto_now_add=True)

    def clean(self):
        if self.age < 0:
            raise ValidationError("Age cannot be negative.")
        if len(self.phone_number) < 10:
            raise ValidationError("Phone number must be at least 10 digits.")

    def __str__(self):
        return self.patient_name



class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)  # Ensure Doctor model is defined
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.TextField()

    def __str__(self):
        return f"{self.patient.user.username} - {self.doctor.user.username} on {self.date}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnosis = models.CharField(max_length=255)
    medications = models.TextField()  # List of medications, separated by commas
    allergies = models.TextField(blank=True)  # List of allergies, separated by commas
    treatment_history = models.TextField()  # History of treatments and surgeries
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Medical Record of {self.patient.user.username} on {self.date}"


class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50, choices=[('Paid', 'Paid'), ('Pending', 'Pending')])
    insurance_info = models.CharField(max_length=255, blank=True)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Billing record for {self.patient.user.username}"


class HealthResource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()  # Link to external resources
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, related_name='prescriptions', on_delete=models.CASCADE)
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    duration = models.IntegerField()  # Duration in days
    refills = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.medication} for {self.appointment.patient.patient_name}"