from rest_framework import serializers
from .transaction_models import *
#from  import MedicineSerializer,SupplierSerializer
#from Hospital.serializers import PatientSerializer

class TransactionSerializer(serializers.ModelSerializer):
    medicine_id=serializers.IntegerField(source="medicine.id",read_only=True)
    medicine_sn=serializers.CharField(source="medicine.serial_number",read_only=True)
    medicine_Unit=serializers.IntegerField(source="medicine.unit_of_measure",read_only=True)
    stock_status=serializers.IntegerField(source="medicine.stock_status",read_only=True)
    batch_id=serializers.IntegerField(source="medicine.batch.id",read_only=True)
    batch_number=serializers.IntegerField(source="medicine.batch.batch_number",read_only=True)
    transaction_type_name=serializers.CharField(source="transaction_type.type_name",read_only=True)
    destination_name=serializers.CharField(source="destination.name",read_only=True)
    destination_location=serializers.CharField(source="destination.location.id",read_only=True)
    source_name=serializers.CharField(source="source.name",read_only=True)
    source_location=serializers.CharField(source="source.location.id",read_only=True)
    
    class Meta:
        model=Transaction
        fields="__all__"

class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields="__all__"
# class AppointmentFeeSerializer(serializers.ModelSerializer):
#     patient=PatientSerializer()
#     transaction=TransactionSerializer()
#     class Meta:
#         model=AppointmentFee
#         fields="__all__"

class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=TransactionType
        fields="__all__"