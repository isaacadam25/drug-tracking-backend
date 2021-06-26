from rest_framework import serializers
from .transaction_models import *
#from  import MedicineSerializer,SupplierSerializer
#from Hospital.serializers import PatientSerializer

class TransactionSerializer(serializers.ModelSerializer):
    batch_number=serializers.IntegerField(source="batch.batch_number",read_only=True)
    transaction_type_name=serializers.CharField(source="transaction_type.type_name",read_only=True)
    destination_number=serializers.CharField(source="location_to.reference_number",read_only=True)
    destination_name=serializers.CharField(source="location_to.name",read_only=True)
    destination_location=serializers.CharField(source="location_to.location.region",read_only=True)
    source_number=serializers.CharField(source="location_from.reference_number",read_only=True)
    source_name=serializers.CharField(source="location_from.name",read_only=True)
    source_location=serializers.CharField(source="location_from.location.region",read_only=True)
    
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