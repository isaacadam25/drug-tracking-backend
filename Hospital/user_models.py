from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HospitalRoom(models.Model):
    room_number=models.CharField(max_length=5)
    description=models.TextField(null=True, blank=True)
    def __str__(self):
        return f"Room {self.room_number}"
class UserType(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField(null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.id}:{self.name}'
class UserProfile(models.Model):
    actual_user=models.OneToOneField(User,on_delete=models.CASCADE)
    user_type=models.ForeignKey(UserType,models.SET_NULL,null=True)
    room=models.OneToOneField(HospitalRoom,on_delete=models.SET_NULL,null=True, related_name="staffs_room")
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    gender=models.BooleanField()
    def __str__(self):
        return f"{self.actual_user.username}"
