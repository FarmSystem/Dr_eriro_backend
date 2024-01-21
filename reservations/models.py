from django.db import models
from patients.models import Patient
from doctors.models import Doctor

# Create your models here.
class Reservation(models.Model):
    status = models.CharField(max_length=1, choices=[('w','대기'),('a','확정'),('d','취소'),('c','완료')])
    visit_for = models.CharField(max_length=100, null=True)
    reservation_date = models.DateTimeField()
    underlying_disease = models.CharField(max_length=200, null=True)
    prescribe = models.CharField(max_length=200, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)