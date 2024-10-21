# views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from .forms import DoctorRegistrationForm, DoctorLoginForm
from patients.models import Appointment,Prescription

def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor registration successful! You can now log in.")
            return redirect('login_doctor')  # Redirect to login page
    else:
        form = DoctorRegistrationForm()
    return render(request, 'doctors/register.html', {'form': form})

def login_doctor(request):
    if request.method == 'POST':
        form = DoctorLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('doctor_dashboard')  # Redirect to the doctor dashboard
            else:
                messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = DoctorLoginForm()
    return render(request, 'doctors/login.html', {'form': form})

def doctor_logout(request):
    logout(request)
    return redirect('login_doctor')

def doctor_dashboard(request):
    doctor = request.user.doctor  # Get the logged-in doctor
    appointments = Appointment.objects.filter(doctor=doctor)  # Get all appointments for the doctor
    patients = Patient.objects.filter(appointment__doctor=doctor).distinct()  # Get distinct patients with appointments

    return render(request, 'doctors/dashboard.html', {'appointments': appointments, 'patients': patients})


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from patients.models import MedicalRecord, Patient


@login_required
def patient_medical_history(request, patient_id):
    # Ensure the user is a doctor, or handle unauthorized access

    # Get the patient object or return a 404 if not found
    patient = get_object_or_404(Patient, id=patient_id)

    # Retrieve medical records for this patient
    records = MedicalRecord.objects.filter(patient=patient)

    return render(request, 'doctors/medical_history.html', {
        'patient': patient,
        'records': records
    })


def prescribe(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == 'POST':
        # Handle prescription logic (you might want to save the prescription to the database)
        return redirect('doctor_dashboard')
    return render(request, 'doctors/prescribe.html', {'appointment': appointment})

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from patients.models import Appointment, Prescription

def save_prescription(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id)

        # Get the form data
        medication = request.POST.get('medication')
        dosage = request.POST.get('dosage')
        instructions = request.POST.get('instructions')
        duration = request.POST.get('duration')
        refills = request.POST.get('refills')

        # Check if all required fields are filled
        if all([medication, dosage, instructions, duration, refills]):
            # Create a new Prescription object
            prescription = Prescription(
                appointment=appointment,
                medication=medication,
                dosage=dosage,
                instructions=instructions,
                duration=duration,
                refills=refills
            )
            prescription.save()
            messages.success(request, 'Prescription saved successfully!')
        else:
            messages.error(request, 'All fields are required.')

        return redirect('doctor_dashboard')  # Redirect to the doctor dashboard or any other page

    # If the request is not POST, redirect or show an error
    messages.error(request, 'Invalid request method.')
    return redirect('doctor_dashboard')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from patients.models import Appointment, MedicalRecord
from .forms import MedicalRecordForm


def create_medical_record(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = appointment.patient  # Link to the patient from the appointment
            medical_record.save()
            messages.success(request, 'Medical record created successfully!')
            return redirect('doctor_dashboard')  # Redirect to an appropriate page
    else:
        form = MedicalRecordForm()

    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'doctors/create_medical_record.html', context)
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from patients.models import Appointment

def accept_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Accepted'  # Update status as needed
    appointment.save()
    messages.success(request, 'Appointment accepted successfully!')
    return redirect('doctor_dashboard')

def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Rejected'  # Update status as needed
    appointment.save()
    messages.success(request, 'Appointment rejected successfully!')
    return redirect('doctor_dashboard')


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from patients.models import Appointment
from django.contrib.auth.decorators import login_required


@login_required
def doctor_schedule(request):
    doctor = request.user.doctor  # Get the doctor associated with the logged-in user
    appointments = Appointment.objects.filter(doctor=doctor).order_by('date',
                                                                      'time')  # Fetch appointments for the doctor

    # Handle filtering
    filter_date = request.GET.get('date', None)
    filter_status = request.GET.get('status', None)
    filter_patient = request.GET.get('patient', None)

    if filter_date:
        appointments = appointments.filter(date=filter_date)
    if filter_status:
        appointments = appointments.filter(status=filter_status)
    if filter_patient:
        appointments = appointments.filter(patient__user__username__icontains=filter_patient)

    context = {
        'appointments': appointments,
        'current_year': timezone.now().year,
        'filter_date': filter_date,
        'filter_status': filter_status,
        'filter_patient': filter_patient,
    }
    return render(request, 'doctors/schedule.html', context)


@login_required
def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        appointment.reason = request.POST.get('reason')
        appointment.status = request.POST.get('status')
        appointment.save()
        messages.success(request, 'Appointment updated successfully!')
        return redirect('doctor_schedule')

    context = {
        'appointment': appointment,
    }
    return render(request, 'doctors/edit_appointment.html', context)


from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


@login_required
def send_appointment_notifications(request):
    # Fetch upcoming appointments within the next 24 hours
    upcoming_appointments = Appointment.objects.filter(date=timezone.now().date(), time__gte=timezone.now().time())

    for appointment in upcoming_appointments:
        subject = 'Upcoming Appointment Reminder'
        message = f'Reminder: You have an appointment with Dr. {appointment.doctor.user.username} on {appointment.date} at {appointment.time}.'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [appointment.patient.user.email])

    # After sending notifications, return a response
    return HttpResponse("Notifications sent successfully.")
def save_appointment_changes(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.status = request.POST.get('status', appointment.status)
        appointment.reason = request.POST.get('reason', appointment.reason)
        appointment.save()
        return redirect('doctor_schedule')  # Redirect to the schedule after saving changes
    return redirect('doctor_schedule')  # Redirect if the request method is not POST


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from patients.models import Billing, Patient
from .forms import BillingForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from patients.models import Patient, Billing
from .forms import BillingForm


def create_billing(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)  # Fetch the patient based on the patient ID

    if request.method == 'POST':
        form = BillingForm(request.POST)

        if form.is_valid():
            billing = form.save(commit=False)  # Don't save to the DB yet
            billing.patient = patient  # Link the billing to the patient
            billing.save()  # Save to the database

            messages.success(request, 'Billing record has been created successfully.')
            return redirect('doctor_dashboard')  # Redirect to the dashboard or relevant page
        else:
            messages.error(request, 'There was an error creating the billing record.')
    else:
        form = BillingForm()

    return render(request, 'doctors/create_billing.html', {'form': form, 'patient': patient})
