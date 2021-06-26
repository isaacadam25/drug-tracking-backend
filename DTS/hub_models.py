from django.db import models
import random


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
    def generate_num():
        
        serials=[]
        new=list(Institute.objects.values_list('reference_number'))
        for n in new:
            for l in n:
                serials.append(l)
        not_unique = True
        while not_unique:
            x = f'INS{random.randint(10000000,99999999)}'
            if x not in serials:
                not_unique=False
        return x
    reference_number=models.CharField(max_length=20,blank=True,editable=False,unique=True,default=generate_num)
    location=models.ForeignKey(Local,on_delete=models.DO_NOTHING)
    institute_type=models.ForeignKey(InstituteType,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return f'{self.name} {self.location.region}'