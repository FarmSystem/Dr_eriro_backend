from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor
from .serializers import DoctorProfileSerializer, DoctorRegistrationSerializer, LoginSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout

class DoctorRegistrationView(APIView):
    def post(self, request):
        serializer = DoctorRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            # Save the new user
            user = serializer.save()

            # Authenticate the user after registration
            authenticated_user = authenticate(request, email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if authenticated_user:
                login(request, authenticated_user)

            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)  # Django의 login 함수를 사용하여 사용자를 로그인합니다.
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        # Django의 logout 함수를 사용하여 사용자를 로그아웃합니다.
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    

class DoctorProfileAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    def get(self, request, doctor_id):
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            serializer = DoctorProfileSerializer(doctor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Doctor.DoesNotExist:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

