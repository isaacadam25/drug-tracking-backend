from .hub_models import *
from rest_framework import serializers

# Create your tests here.
class InstituteSerializer(serializers.ModelSerializer):
    location_region=serializers.CharField(source="location.region",read_only=True)
    location_city=serializers.CharField(source="location.city",read_only=True)
    institute_type_name=serializers.CharField(source="institute_type.name",read_only=True)
    class Meta:
        model=Institute
        fields='__all__'

class DistributionSerializer(serializers.ModelSerializer):
    location_region=serializers.CharField(source="location.region",read_only=True)
    location_city=serializers.CharField(source="location.city",read_only=True)
    institute_type_name=serializers.CharField(source="institute_type.name",read_only=True)
    class Meta:
        model=Institute
        fields='__all__'
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Local
        fields='__all__'