from django.db import models
from .user_models import UserProfile as User
import random
import sys

count=0
def create_new_ref_number():
    global count
    count=count+1
    return f'PT{count+10000000}'
# Create your models here.
class PatientType(models.Model):
    name=models.CharField(max_length=30)
    description=models.TextField(null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    def __str__(self):
       return f"{self.name}"

class Patient(models.Model):
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    other_name=models.CharField(max_length=20,null=True, blank=True)
    is_male=models.BooleanField()
    def generate_num():
        
        serials=[]
        new=list(Patient.objects.values_list('serial_number'))
        for n in new:
            for l in n:
                serials.append(l)
        not_unique = True
        while not_unique:
            x = f'PT{random.randint(10000000,99999999)}'
            if x not in serials:
                not_unique=False
        return x
            
    serial_number=models.CharField(max_length=10,blank=True,editable=False,unique=True,default=generate_num)
    dob=models.DateField()
    patient_type=models.ForeignKey(PatientType,on_delete=models.PROTECT)
    address=models.CharField(max_length=20)
    contacts=models.CharField(max_length=20,null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    description=models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.serial_number}: {self.first_name} {self.last_name}"

class Appointment(models.Model):
    patient_number=models.ForeignKey(Patient,on_delete=models.PROTECT)
    def generate_num():
        
        serials=[]
        new=list(Appointment.objects.values_list('appointment_number'))
        for n in new:
            for l in n:
                serials.append(l)
        not_unique = True
        while not_unique:
            x = f'AP{random.randint(10000000,99999999)}'
            if x not in serials:
                not_unique=False
        return x
    appointment_number=models.CharField(max_length=10,blank=True,editable=False,unique=True,default=generate_num)
    status_options=(('pending','Pending'),('active','Active'),('complete','Complete'))
    status=models.CharField(max_length=10,choices = status_options,default='pending',blank=True)
    date_of_appointment=models.DateField(auto_now_add=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    description=models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.patient_number.first_name} {self.patient_number.last_name}"


class Labtest(models.Model):
    appointment=models.ForeignKey(Appointment,on_delete=models.CASCADE)
    technician=models.ForeignKey(User,on_delete=models.PROTECT)
    date_of_test=models.DateTimeField(auto_now=True)
    description=models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.id}"

class LabTestItem(models.Model):
    name=models.CharField(max_length=20)
    results=models.TextField()
    comments=models.TextField()
    test=models.ForeignKey(Labtest,on_delete=models.CASCADE)
    description=models.TextField(null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name} {self.labtest}"

class Diagnosis(models.Model):
    appointment=models.ForeignKey(Appointment,on_delete=models.CASCADE)
    diagnoses=models.TextField(null=True)
    complaints=models.TextField()
    description=models.TextField(null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
           


    