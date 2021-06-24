from rest_framework import serializers
from .pharmacy_models import Medicine,MSDZone,Batch, MedicineBrand,Supplier
from .user_models import UserProfile as User
from rest_framework import serializers

class MedicineBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=MedicineBrand
        fields=['id','brand_name']
class BatchSerializer(serializers.ModelSerializer):
    medicine_brand=MedicineBrandSerializer()
    class Meta:
        model=Batch
        fields=['id','batch_number','medicine_brand','medicine_name']
class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model=MSDZone
        fields=['id','zone_name','zone-location']
class MedicineSerializer(serializers.ModelSerializer):
    batch=BatchSerializer()
    msd_zone=ZoneSerializer()
    class Meta:
        model=Medicine
        fields='__all__'
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model=Supplier
        fields='__all__'