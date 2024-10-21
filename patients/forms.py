import datetime
from django import forms
from .models import Patient, Appointment
from django.contrib.auth.models import User
from django.utils import timezone
from doctors.models import Doctor

from django import forms
from django.core.validators import EmailValidator
from .models import Patient


class PatientRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', min_length=8)
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password', min_length=8)

    class Meta:
        model = Patient
        exclude = ['user']  # Exclude the user field as it will be created in the view
        fields = [
            'patient_id',
            'patient_name',
            'age',
            'gender',
            'height',
            'weight',
            'address',
            'phone_number',
            'email'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        # Check if passwords match
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")

        # Optionally, you can add additional password validation here
        if password and len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        # Validate email format if needed
        email = cleaned_data.get("email")
        if email:
            email_validator = EmailValidator()
            try:
                email_validator(email)
            except forms.ValidationError:
                raise forms.ValidationError("Enter a valid email address.")

        return cleaned_data  # Ensure to return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if the email already exists in the Patient model
        if Patient.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)

        self.fields['doctor'] = forms.ModelChoiceField(
            queryset=Doctor.objects.all(),  # Fetch all doctors
            label="Select Doctor",
            empty_label="Select a doctor",
            required=True
        )

        self.fields['date'] = forms.DateField(
            widget=forms.DateInput(attrs={
                'class': 'flatpickr',  # Class to initialize Flatpickr
                'placeholder': 'Select date',
                'autocomplete': 'off'
            }),
            label='Date',
        )

        self.fields['time'] = forms.TimeField(
            widget=forms.TimeInput(attrs={
                'type': 'time',  # HTML5 time input
                'placeholder': 'Select time',
            }),
            label='Time',
        )

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        # Ensure the appointment is not in the past
        if date and time:
            # Combine date and time to create a datetime object
            appointment_datetime = timezone.make_aware(datetime.datetime.combine(date, time))

            if appointment_datetime < timezone.now():
                raise forms.ValidationError("Appointment cannot be scheduled in the past.")

        return cleaned_data

