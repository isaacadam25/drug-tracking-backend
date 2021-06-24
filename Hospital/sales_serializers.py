from rest_framework import serializers
from .sales_models import Order, OrderedItem,Invoice,OrderType,Invoice,Transaction,AppointmentFee
from .pharmacy_serializers import MedicineSerializer,SupplierSerializer
from .hospital_serializers import PatientSerializer

class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderType()
        fields="__all__"
class OrderSerializer(serializers.ModelSerializer):
    ordertype_name=serializers.CharField(source="order_type.name",read_only=True)
    supplier_name=serializers.CharField(source="supplier.name",read_only=True)
    supplier_location=serializers.CharField(source="supplier.location",read_only=True)
    class Meta:
        model=Order
        fields="__all__"
    
class ItemSerializer(serializers.ModelSerializer):
    order_supplier=serializers.CharField(source="order.supplier",read_only=True)
    order_totalquantity=serializers.CharField(source="order.total_quantity",read_only=True)
    order_supplier=serializers.CharField(source="order.supplier",read_only=True)
    supplier_name=serializers.CharField(source="supplier.name",read_only=True)
    class Meta:
        model=OrderedItem
        fields="__all__"

class InvoiceSerializer(serializers.ModelSerializer):
    order=OrderSerializer()
    class Meta:
        model=Invoice
        fields="__all__"

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields="__all__"
class AppointmentFeeSerializer(serializers.ModelSerializer):
    patient=PatientSerializer()
    transaction=TransactionSerializer()
    class Meta:
        model=AppointmentFee
        fields="__all__"