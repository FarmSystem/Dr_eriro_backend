from rest_framework import serializers
from .models import Doctor, Hospital, Subject

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['email', 'name', 'gender', 'location', 'number', 'photo', 'hospital', 'subject', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'location']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'large_name', 'detail_name']

class DoctorProfileSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'gender', 'photo', 'location', 'hospital', 'subject'
        ]

