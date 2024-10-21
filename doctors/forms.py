# forms.py

from django import forms
from django.contrib.auth.models import User
from .models import  Doctor



class DoctorRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = Doctor
        fields = ['specialty', 'license_number']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        doctor = super().save(commit=False)
        doctor.user = user
        if commit:
            doctor.save()
        return doctor

# Doctor Login Form
class DoctorLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())

from django import forms
from patients.models import MedicalRecord

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'medications', 'allergies', 'treatment_history']

        widgets = {
            'diagnosis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Diagnosis'}),
            'medications': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List of Medications'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List of Allergies (if any)'}),
            'treatment_history': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Treatment History'}),
        }

# forms.py
from django import forms
from patients.models import Billing

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['bill_amount', 'payment_status', 'insurance_info', 'payment_date']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'})  # Ensures a date picker is used
        }