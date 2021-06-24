from django.db import models
from django.contrib.auth.models import User
from .hub_models import Local,Institute
# Create your models here.


class UserType(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField(null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.id}:{self.name}'

class UserProfile(models.Model):
    actual_user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='system_users')
    title=models.CharField(max_length=30)
    user_type=models.ForeignKey(UserType,on_delete=models.SET_NULL,null=True)
    organization=models.ForeignKey(Institute,on_delete=models.SET_NULL,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.actual_user.username}"
