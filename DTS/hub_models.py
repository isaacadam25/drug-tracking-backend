from django.db import models


# Create your models here.
class InstituteType(models.Model):
    name=models.CharField(max_length=30)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.name}'
class Local(models.Model):
    zone=models.CharField(max_length=30)
    region=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    region=models.CharField(max_length=30)
    area=models.CharField(max_length=30,blank=True,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.area},{self.city},{self.region}'

class Institute(models.Model):
    name=models.CharField(max_length=30)
    location=models.ForeignKey(Local,on_delete=models.DO_NOTHING)
    institute_type=models.ForeignKey(InstituteType,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return f'{self.name} {self.location.region}'