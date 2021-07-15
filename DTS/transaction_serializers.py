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
    drug_name=serializers.CharField(source="batch.medicine_detail.name",read_only=True)
    drug_manufacturer=serializers.CharField(source="batch.medicine_detail.manufacturer",read_only=True)
    drug_type=serializers.CharField(source="batch.medicine_type.type_name",read_only=True)
    quantity_measure=serializers.CharField(source="batch.unit_of_measure",read_only=True)
    concentration=serializers.CharField(source="batch.concentration",read_only=True)
    production_date=serializers.CharField(source="batch.production_date",read_only=True)
    expiry_date=serializers.CharField(source="batch.expiry_date",read_only=True)


    class Meta:
        model=Transaction
        fields="__all__"
class AcceptTransactionSerializer(serializers.ModelSerializer):
    source_name=serializers.CharField(source="location_from.name",read_only=True)
    source_location=serializers.CharField(source="location_from.location.region",read_only=True)
    class Meta:
        model=Transaction
        exclude=['id','transaction_type','batch','location_to','location_from','date_added','date_modified']

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

class ExpiredTableSerializer(serializers.ModelSerializer):
    class Meta:
        model=ExpiredTable
        fields="__all__"