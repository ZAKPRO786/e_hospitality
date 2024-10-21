from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from doctors.models import Doctor
from patients.models import Patient, Appointment
from .forms import DoctorForm, PatientForm, AppointmentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Admin
from .forms import AdminRegisterForm, AdminLoginForm



# Admin Registration View
def admin_register(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # This will save both User and Admin
            # Authenticate and log in the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('admin_dashboard')  # Adjust 'admin_dashboard' if needed
    else:
        form = AdminRegisterForm()
    return render(request, 'admins/register.html', {'form': form})



# Admin Login View
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AdminLoginForm()
    return render(request, 'admins/login.html', {'form': form})


# Admin Logout View
@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')


# Doctor Views
@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'admins/doctor_list.html', {'doctors': doctors})

@login_required
def doctor_create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'admins/doctor_form.html', {'form': form})

@login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'admins/doctor_form.html', {'form': form})

@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.delete()
        return redirect('doctor_list')
    return render(request, 'admins/doctor_confirm_delete.html', {'doctor': doctor})

# Patient Views
@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'admins/patient_list.html', {'patients': patients})

@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'admins/patient_form.html', {'form': form})

@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'admins/patient_form.html', {'form': form})

@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'admins/patient_confirm_delete.html', {'patient': patient})

# Appointment Views
@login_required
def appointment_list(request):
    appointments = Appointment.objects.all()
    return render(request, 'admins/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'admins/appointment_form.html', {'form': form})

@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'admins/appointment_form.html', {'form': form})

@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
    return render(request, 'admins/appointment_confirm_delete.html', {'appointment': appointment})

# Dashboard View
@login_required
def admin_dashboard(request):
    doctor_count = Doctor.objects.count()
    patient_count = Patient.objects.count()
    appointment_count = Appointment.objects.count()
    recent_appointments = Appointment.objects.all().order_by('-date')[:5]  # Display last 5 appointments

    context = {
        'doctor_count': doctor_count,
        'patient_count': patient_count,
        'appointment_count': appointment_count,
        'recent_appointments': recent_appointments,
    }
    return render(request, 'admins/dashboard.html', context)
