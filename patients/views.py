from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from .forms import PatientRegistrationForm, AppointmentForm
from .models import Appointment, MedicalRecord, Billing, HealthResource, Patient,Prescription
from rest_framework import viewsets
from .serializers import PatientSerializer, AppointmentSerializer, MedicalRecordSerializer, BillingSerializer, HealthResourceSerializer

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import PatientRegistrationForm  # Make sure to import your form


def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            # Proceed with user creation and registration
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, "A user with this email already exists.")
                return render(request, 'patients/register.html', {'form': form})

            # Create User instance
            user = User.objects.create_user(
                username=email,
                email=email,
                password=form.cleaned_data['password']
            )

            # Create Patient instance
            patient = form.save(commit=False)
            patient.user = user
            patient.save()

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login_patient')
        else:
            # If the form is invalid, you can provide specific error messages if needed
            messages.error(request, "Please correct the errors below.")
    else:
        form = PatientRegistrationForm()

    return render(request, 'patients/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('patient_dashboard')  # Redirect to the patient dashboard
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    return render(request, 'patients/login.html')
@login_required
def patient_logout(request):
    logout(request)
    return redirect('login_patient')

@login_required  # Protect this view
def patient_dash(request):
    # Assuming the user is linked to the Patient model
    patient = request.user.patient  # Get the associated Patient object

    # Retrieve the patient's appointments, medical records, and bills
    appointments = Appointment.objects.filter(patient=patient)
    medical_records = MedicalRecord.objects.filter(patient=patient)
    bills = Billing.objects.filter(patient=patient)

    # Retrieve prescriptions related to the patient's appointments
    prescriptions = Prescription.objects.filter(appointment__in=appointments)

    # Prepare context data for rendering
    context = {
        'patient': patient,
        'appointments': appointments,
        'medical_records': medical_records,
        'bills': bills,
        'prescriptions': prescriptions,
    }

    # Render the patient dashboard template with context data
    return render(request, 'patients/dashboard.html', context)

@login_required  # Protect this view
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient  # Associate with logged-in patient
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('patient_dashboard')  # Redirect to patient dashboard
    else:
        form = AppointmentForm()

    return render(request, 'patients/book_appointment.html', {'form': form})



@login_required  # Protect this view
def billing_payments(request):
    bills = Billing.objects.filter(patient=request.user.patient)
    return render(request, 'patients/billing_payments.html', {'bills': bills})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
import stripe
from django.conf import settings
from .models import Billing  # Adjust the import according to your project structure
from django.urls import reverse

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import stripe
from .models import Billing
@login_required
def pay_bill(request, bill_id):
    bill = get_object_or_404(Billing, id=bill_id)

    if request.method == "POST":
        stripe.api_key = settings.STRIP_SECRET_KEY

        try:
            # Create a Checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',  # Change to your desired currency
                        'product_data': {
                            'name': f'Billing for {bill.patient.user.username}',
                        },
                        'unit_amount': int(bill.bill_amount * 100),  # Amount in cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('success')) + '?bill_id=' + str(bill.id),  # Success URL after payment
                cancel_url=request.build_absolute_uri(reverse('cancel')),  # Cancel URL
            )

            return redirect(checkout_session.url, code=303)  # Redirect to Stripe Checkout session
        except Exception as e:
            messages.error(request, f'Payment failed: {str(e)}')  # Handle error gracefully

    return render(request, 'patients/pay_bill.html', {'bill': bill})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Billing

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Billing  # Adjust this import based on your project structure


def payment_success(request):
    # Assuming you have a way to determine which bill is being paid
    bill_id = request.GET.get(
        'bill_id')  # Get the bill ID from the request (you'll need to include this in the success URL)

    if bill_id:
        bill = get_object_or_404(Billing, id=bill_id)

        # Update the billing record to set as paid
        bill.payment_status = 'Paid'
        bill.payment_date = timezone.now()  # Set payment date
        bill.save()

        messages.success(request, 'Payment successful! Your bill has been paid.')

        # Render a success page with the bill details
        return render(request, 'patients/payment_success.html', {'bill': bill})

    else:
        messages.error(request, 'Bill ID not found.')
        return redirect('cancel')  # Redirect to a default view if bill ID is not found


def payment_cancel(request):
    messages.warning(request, 'Payment was canceled. Please try again.')
    return render(request, 'patients/payment_cancel.html')  # Render a cancel page or redirect as necessary



@login_required  # Protect this view
def health_resources(request):
    resources = HealthResource.objects.all()
    return render(request, 'patients/health_resources.html', {'resources': resources})


# REST API ViewSets
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()  # Ensure the queryset is defined
    serializer_class = PatientSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer


class BillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer


class HealthResourceViewSet(viewsets.ModelViewSet):
    queryset = HealthResource.objects.all()
    serializer_class = HealthResourceSerializer
def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment rescheduled successfully!')
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'patients/reschedule_appointment.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Appointment  # Import your Appointment model

def cancel_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id)

        # Delete the appointment
        appointment.delete()

        # Add a success message
        messages.success(request, 'Appointment cancelled successfully!')
        return redirect('patient_dashboard')

    # If the request is not POST, redirect to the dashboard
    return redirect('patient_dashboard')


def index(request):
    return render(request,'patients/index.html')