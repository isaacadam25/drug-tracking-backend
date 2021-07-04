from rest_framework import serializers
from .stock_models import Approval,Batch,MedicineDetails,MedicineType
from .user_models import *

# class MedicineBrandSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=MedicineBrand
#         fields=['id','brand_name']
class BatchSerializer(serializers.ModelSerializer):
    #approver=serializers.CharField(source="approval.approver",read_only=True)
    approval_status=serializers.CharField(source="approval.status",read_only=True)
    type_name=serializers.CharField(source="medicine_type.type_name",read_only=True)
    medicine_name=serializers.CharField(source="medicine_detail.name",read_only=True)
    medicine_manufacturer=serializers.CharField(source="medicine_detail.manufacturer",read_only=True)
    
    class Meta:
        model=Batch
        fields='__all__'

class AcceptBatchSerializer(serializers.ModelSerializer):
    #approver=serializers.CharField(source="approval.approver",read_only=True)
    approval_status=serializers.CharField(source="approval.status",read_only=True)
    type_name=serializers.CharField(source="medicine_type.type_name",read_only=True)
    medicine_name=serializers.CharField(source="medicine_detail.name",read_only=True)
    medicine_manufacturer=serializers.CharField(source="medicine_detail.manufacturer",read_only=True)
    
    class Meta:
        model=Batch
        exclude=['id','quantity_received','date_added','date_modified','medicine_detail','medicine_type']


class BatchApprovalSerializer(serializers.ModelSerializer):
    batch_number=serializers.IntegerField(source="id.batch_number",read_only=True)
    unit_measure=serializers.IntegerField(source="id.unit_of_measure",read_only=True)
    quantity_received=serializers.IntegerField(source="id.quantity_received",read_only=True)
    expiry_date=serializers.CharField(source="id.expiry_date",read_only=True)
    production_date=serializers.CharField(source="id.production_date",read_only=True)
    concentration=serializers.CharField(source="id.concentration",read_only=True)
    manufacturer=serializers.CharField(source="id.medicine_detail.manufacturer",read_only=True)
    drug_name=serializers.CharField(source="id.medicine_detail.name",read_only=True)
    type=serializers.CharField(source="id.medicine_type.type_name",read_only=True)
    medicine_type=serializers.CharField(source="id.medicine_type.type_name",read_only=True)
    class Meta:
        model=Approval
        fields='__all__'

class MedicineInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model=MedicineDetails
        fields='__all__'


class MedicineTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=MedicineType
        fields='__all__'
# class ZoneSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=MSDZone
#         fields=['id','zone_name','zone-location']


# class ApprovalSerializer(serializers.ModelSerializer):
#     #approver_name=serializers.IntegerField(source="approver.actual_user.username",read_only=True)
#     approver_title=serializers.IntegerField(source="approver.title",read_only=True)

#     class Meta:
#         models=Medicine
#         fields='__all__'
# # class SupplierSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Supplier
#         fields='__all__'