from rest_framework import serializers
from Hospital.user_models import UserProfile,HospitalRoom,UserType
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['password'])
        return user

class HospitalRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model=HospitalRoom
        fields="__all__"

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserType
        fields='__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"
class UserProfileSerializer(serializers.ModelSerializer):
    room_number=serializers.CharField(source="room.room_number",read_only=True)
    usertype_name=serializers.CharField(source="user_type.name",read_only=True)
    first_name=serializers.CharField(source="actual_user.first_name",read_only=True)
    username=serializers.CharField(source="actual_user.username",read_only=True)
    last_name=serializers.CharField(source="actual_user.last_name",read_only=True)
    is_staff=serializers.BooleanField(source="actual_user.is_staff",read_only=True)
    is_active=serializers.BooleanField(source="actual_user.is_active",read_only=True)
    usertype_description=serializers.CharField(source="user_type.description",read_only=True)
    password=serializers.CharField(source="actual_user.password",read_only=True)
    class Meta:
        model=UserProfile
        fields='__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
