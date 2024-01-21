from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views
from .views import PatientListAPIView

app_name = 'patients'


urlpatterns = [
    path('patient-list/', PatientListAPIView.as_view(), name='patient-list'),
]