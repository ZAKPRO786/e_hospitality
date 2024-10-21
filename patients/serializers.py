# serializers.py

from rest_framework import serializers
from .models import Patient, Appointment, MedicalRecord, Billing, HealthResource

# Serializer for Patient Model
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'user', 'patient_name', 'age', 'address', 'phone_number', 'email']  # Adjusted field names

    def validate_email(self, value):
        if Patient.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address is already in use.")
        return value

# Serializer for Appointment Model
class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)  # Nested serialization

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date', 'time', 'reason']

    def create(self, validated_data):
        patient = self.context['request'].user.patient  # Get the patient from the request
        validated_data['patient'] = patient
        return super().create(validated_data)

# Serializer for MedicalRecord Model
class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)  # Nested serialization

    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'diagnosis', 'medications', 'allergies', 'treatment_history', 'date']

# Serializer for Billing Model
class BillingSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)  # Nested serialization

    class Meta:
        model = Billing
        fields = ['id', 'patient', 'bill_amount', 'payment_status', 'insurance_info', 'payment_date']

# Serializer for HealthResource Model
class HealthResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthResource
        fields = ['id', 'title', 'description', 'link', 'created_at']
