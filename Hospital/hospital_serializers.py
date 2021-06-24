from rest_framework import serializers
from .hospital_models import *
from .user_serializers import UserProfileSerializer,UserSerializer
# from Pharmacy.serializers import MedicineBrandSerializer
from rest_framework import serializers

class PatientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=PatientType
        fields=['id','name','description']
class PatientSerializer(serializers.ModelSerializer):
    # patient_type=PatientTypeSerializer()
    class Meta:
        model=Patient
        fields='__all__'
class AppointmentSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(source="patient_number.first_name",read_only=True)
    last_name=serializers.CharField(source="patient_number.last_name",read_only=True)
    patient_sn=serializers.CharField(source="patient_number.serial_number",read_only=True)
    class Meta:
        model=Appointment
        fields='__all__'
class LabtestSerializer(serializers.ModelSerializer):
    # appointment=AppointmentSerializer()
    # technician=UserSerializer()
    class Meta:
        model=Labtest
        fields='__all__'
class LabTestItemSerializer(serializers.ModelSerializer):
    # test=LabtestSerializer()
    class Meta:
        model=LabTestItem
        fields='__all__'
class DiagnosisSerializer(serializers.ModelSerializer):
    # appointment=AppointmentSerializer()
    class Meta:
        model=Diagnosis
        fields='__all__'