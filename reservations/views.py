from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from .serializers import ReservationWithPatientSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

class PatientListAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    
    def get(self, request, doctor_id):
        reservations = Reservation.objects.filter(doctor_id=doctor_id)
        serializer = ReservationWithPatientSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReservationListAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    
    def get(self, _, doctor_id):
        reservations = Reservation.objects.filter(doctor_id=doctor_id, status__in=['a', 'w'])
        serializer = ReservationWithPatientSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
from django.db import close_old_connections

@csrf_exempt
@require_POST
def update_reservation_state(request):
    try:
        reservation_id = request.GET.get('reservation_id')
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return JsonResponse({'error': 'Reservation not found'}, status=404)

    new_state = request.GET.get('new_state')

    if new_state == '1':
        reservation.status = 'a'
    elif new_state == '0':
        reservation.status = 'd'
    else:
        return JsonResponse({'error': 'Invalid new_state value'}, status=400)

    reservation.save()

    # 데이터베이스 연결 닫기
    close_old_connections()

    return JsonResponse({'success': 'Reservation status updated successfully'}, status=200)
