from rest_framework import serializers
from patients.serializers import PatientSerializer
from .models import Reservation
from patients.models import Patient

class ReservationWithPatientSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = Reservation
        fields = '__all__'
