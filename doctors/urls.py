# urls.py

from django.urls import path
from .views import register_doctor, login_doctor, doctor_dashboard, prescribe,save_prescription,create_medical_record,accept_appointment,reject_appointment
from .views import edit_appointment,doctor_schedule,save_appointment_changes,send_appointment_notifications,create_billing,doctor_logout,patient_medical_history
urlpatterns = [
    path('register/', register_doctor, name='register_doctor'),
    path('login/', login_doctor, name='login_doctor'),
    path('logout/', doctor_logout, name='logout_doctor'),
    path('dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('medicalhistory/<int:patient_id>',patient_medical_history, name='patient_medical_history'),
    path('prescribe/<int:appointment_id>/', prescribe, name='prescribe'),
    path('saveprescribe/<int:appointment_id>/', save_prescription, name='save_prescription'),
    path('appointments/<int:appointment_id>/create-medical-record/',create_medical_record, name='create_medical_record'),
    path('appointments/<int:appointment_id>/accept/', accept_appointment, name='accept_appointment'),
    path('appointments/<int:appointment_id>/reject/', reject_appointment, name='reject_appointment'),
    path('schedule/',doctor_schedule, name='doctor_schedule'),
    path('appointments/<int:appointment_id>/edits/', edit_appointment, name='edit_appointment'),
    path('appointments/<int:appointment_id>/save/', save_appointment_changes, name='save_appointment_changes'),
    path('send-notifications/', send_appointment_notifications, name='send_notifications'),
    path('patients/<int:patient_id>/create-billing/', create_billing, name='create_billing'),
]
