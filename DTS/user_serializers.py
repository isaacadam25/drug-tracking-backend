from django.db.models import fields
from .user_models import UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User
from .user_models import *
from knox.models import AuthToken

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','username','password')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['password'])
        return user
class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserType
        fields="__all__"
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        models=User
        fields='__all__'
class UserProfileSerializer(serializers.ModelSerializer):
    usertype_name=serializers.CharField(source="user_type.name",read_only=True)
    first_name=serializers.CharField(source="actual_user.first_name",read_only=True)
    username=serializers.CharField(source="actual_user.username",read_only=True)
    last_name=serializers.CharField(source="actual_user.last_name",read_only=True)
    is_staff=serializers.BooleanField(source="actual_user.is_staff",read_only=True)
    superuser_id=serializers.IntegerField(source="actual_user.id",read_only=True)
    is_active=serializers.BooleanField(source="actual_user.is_active",read_only=True)
    usertype_description=serializers.CharField(source="user_type.description",read_only=True)
    password=serializers.CharField(source="actual_user.password",read_only=True)
    location_region=serializers.CharField(source="organization.location.region",read_only=True)
    location_city=serializers.CharField(source="organization.location.city",read_only=True)
    organization_name=serializers.CharField(source="organization.name",read_only=True)
    organization_type=serializers.CharField(source="organization.institute_type.name",read_only=True)
    
    class Meta:
        model=UserProfile
        fields="__all__"
class RestrictedUserSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(source="actual_user.first_name",read_only=True)
    last_name=serializers.CharField(source="actual_user.last_name",read_only=True)
    is_active=serializers.BooleanField(source="actual_user.is_active",read_only=True)
    location_zone=serializers.CharField(source="location.zone",read_only=True)
    location_region=serializers.CharField(source="location.region",read_only=True)
    location_city=serializers.CharField(source="location.city",read_only=True)
    location_area=serializers.CharField(source="location.area",read_only=True)      
    class Meta:
        model=UserProfile
        fields=['id']