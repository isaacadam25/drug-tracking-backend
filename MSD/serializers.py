from rest_framework import serializers
from .models import *

class MedicineSerializer(serializers.ModelSerializer):

    batch_number=serializers.IntegerField(source="batch.batch_number",read_only=True)
    unit_measure=serializers.IntegerField(source="batch.unit_of_measure",read_only=True)
    tmda_status=serializers.BooleanField(source="batch.approval.status",read_only=True)
    expiry_date=serializers.CharField(source="batch.expiry_date",read_only=True)
    production_date=serializers.CharField(source="batch.production_date",read_only=True)
    concentration=serializers.CharField(source="batch.concentration",read_only=True)
    manufacturer=serializers.CharField(source="batch.medicine_detail.manufacturer",read_only=True)
    drug_name=serializers.CharField(source="batch.medicine_detail.name",read_only=True)
    type=serializers.CharField(source="batch.medicine_type.type_name",read_only=True)
    medicine_type=serializers.CharField(source="batch.medicine_type.type_name",read_only=True)
    class Meta:
        model=Medicine
        fields='__all__'


# class OrderTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=OrderType
#         fields="__all__"
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"
    
class ItemSerializer(serializers.ModelSerializer):
    order_totalquantity=serializers.CharField(source="order.total_quantity",read_only=True)
    order_destination=serializers.CharField(source="order.supplier",read_only=True)
    supplier_name=serializers.CharField(source="supplier.name",read_only=True)
    class Meta:
        model=OrderedItem
        fields="__all__"