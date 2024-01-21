from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views

app_name = 'reservations'

urlpatterns = [
    path('patientList/<int:doctor_id>/', PatientListAPIView.as_view(), name='patientList'),
    path('reservationList/<int:doctor_id>/', ReservationListAPIView.as_view(), name='reservationList'),
    path('update-reservation-state/', update_reservation_state, name='update-reservation-state'),
]