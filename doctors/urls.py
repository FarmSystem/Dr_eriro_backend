from django.urls import path
from .views import DoctorProfileAPIView, DoctorRegistrationView, LoginView, LogoutView

urlpatterns = [
    path('register/', DoctorRegistrationView.as_view(), name='doctor-register'),
    path('login/', LoginView.as_view(), name='doctor-login'),
    path('logout/', LogoutView.as_view(), name='doctor-logout'),
    path('doctor-profile/<int:doctor_id>/', DoctorProfileAPIView.as_view(), name='doctor-profile'),
]
