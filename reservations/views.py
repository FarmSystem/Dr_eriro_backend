from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from .serializers import ReservationWithPatientSerializer, PatientSerializer, ReservationUpdateSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny

# 예약 리스트 조회 (예약 대기, 확정, 완료)
class PatientListAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    
    def get(self, request, doctor_id):
        reservations = Reservation.objects.filter(doctor_id=doctor_id)
        serializer = ReservationWithPatientSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 통합 진료 조회 (예약 대기, 확정만)
class ReservationListAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    
    def get(self, _, doctor_id):
        reservations = Reservation.objects.filter(doctor_id=doctor_id, status__in=['a', 'w'])
        serializer = ReservationWithPatientSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
from django.db import close_old_connections

# 예약 대기 -> 확정/취소
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

# 환자 상세정보 조회
class PatientDetailsAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    
    def get(self, request, patient_id):
        reservations = Reservation.objects.filter(patient_id=patient_id)
        serializer = ReservationWithPatientSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
 # 진료 정보 업데이트   
class UpdateExaminationAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    
    def post(self, request, reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            return JsonResponse({'error': '예약이 없습니다.'}, status=404)

        # (진료중) 의사가 파악한 증상으로 기존의 값 업데이트
        reservation.underlying_disease = request.data.get('underlying_disease', '')

        # 상병 및 처방으로 값 저장
        serializer = ReservationUpdateSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            # 상병과 처방이 비어 있는 경우에만 값을 업데이트
            if not reservation.visit_for:
                reservation.visit_for = request.data.get('visit_for', '')
            if not reservation.prescribe:
                reservation.prescribe = request.data.get('prescribe', '')
            
            reservation.save()
            return JsonResponse({'success': '진료 정보가 성공적으로 업데이트되었습니다.'}, status=200)
        else:
            return JsonResponse({'error': serializer.errors}, status=400)