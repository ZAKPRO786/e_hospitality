from django import forms
from doctors.models import Doctor
from patients.models import Patient, Appointment

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['user', 'specialty', 'license_number', 'schedule']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['user', 'patient_id', 'patient_name', 'age', 'gender', 'height', 'weight', 'address', 'phone_number', 'email']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'time', 'reason', 'status']
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Admin

class AdminRegisterForm(UserCreationForm):
    employee_id = forms.CharField(max_length=20, help_text='Unique ID for admin staff')
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    position = forms.CharField(max_length=50, required=False)
    hire_date = forms.DateField(required=False, widget=forms.SelectDateWidget)

    class Meta:
        model = User  # Use User here for authentication purposes
        fields = ('username', 'password1', 'password2')  # Only include User fields here

    def save(self, commit=True):
        # Save the user part first
        user = super().save(commit=commit)  # Save the User instance
        # Now create the Admin profile instance
        Admin.objects.create(
            user=user,
            employee_id=self.cleaned_data['employee_id'],
            phone_number=self.cleaned_data.get('phone_number', ''),
            address=self.cleaned_data.get('address', ''),
            position=self.cleaned_data.get('position', ''),
            hire_date=self.cleaned_data.get('hire_date', None)
        )
        return user


class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['user', 'employee_id', 'phone_number', 'address', 'position', 'hire_date']
