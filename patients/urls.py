from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'patients', views.PatientViewSet)  # Make sure to use the correct viewset
router.register(r'appointments', views.AppointmentViewSet)
router.register(r'medical-records', views.MedicalRecordViewSet)
router.register(r'billing', views.BillingViewSet)
router.register(r'health-resources', views.HealthResourceViewSet)

urlpatterns = [
    path('register/', views.register_patient, name='register_patient'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('reschedule/<int:appointment_id>/',views.reschedule_appointment, name='reschedule_appointment'),
    path('cancel/',views.cancel_appointment, name='cancel_appointment'),
    path('billing-payments/', views.billing_payments, name='billing_payments'),
    path('pay-bill/<int:bill_id>/', views.pay_bill, name='pay_bill'),
    path('health-resources/', views.health_resources, name='health_resources'),
    path('dashboard/', views.patient_dash, name='patient_dashboard'),
    path('login/', views.login_view, name='login_patient'),
    path('logout/', views.patient_logout, name='logout_patient'),
    path('payment-success/', views.payment_success, name='success'),  # URL for successful payment
    path('payment-cancel/', views.payment_cancel, name='cancel'),
    path('',views.index,name='index'),

    # Include the router URLs
    path('api/', include(router.urls)),  # API endpoints prefixed with /api/
]
