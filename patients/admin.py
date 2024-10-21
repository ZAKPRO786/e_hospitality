# admin.py for patients app

from django.contrib import admin
from .models import Patient, Appointment, MedicalRecord, Billing, HealthResource, Prescription

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'age', 'gender', 'phone_number', 'email', 'registration_date')
    search_fields = ('patient_name', 'email', 'patient_id')
    list_filter = ('gender', 'registration_date')
    ordering = ('patient_name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    search_fields = ('patient__patient_name', 'doctor__user__username')
    list_filter = ('status', 'date')
    ordering = ('-date', 'time')

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'diagnosis', 'date')
    search_fields = ('patient__patient_name', 'diagnosis')
    list_filter = ('date',)

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'bill_amount', 'payment_status', 'insurance_info', 'payment_date')
    search_fields = ('patient__patient_name', 'payment_status', 'insurance_info')
    list_filter = ('payment_status', 'payment_date')
    ordering = ('-payment_date',)

@admin.register(HealthResource)
class HealthResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'medication', 'dosage', 'duration', 'refills')
    search_fields = ('appointment__patient__patient_name', 'medication')
    ordering = ('-appointment__date',)
from django.contrib import admin

# Register your models here.
