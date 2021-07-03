
from django.contrib import admin
from .user_models import *
from .pharmacy_models import *
from .hospital_models import *
from .sales_models import *
# Register your models here.
usermodels=[UserProfile,UserType,HospitalRoom]
salesmodels=[Order,Transaction,OrderType,OrderedItem,Invoice,AppointmentFee]
pharmamodels=[MedicineBrand,HospitalBatch,HospitalMedicine,MSDZone,Supplier]
hospitalmodels=[Patient,PatientType,Appointment,Labtest,LabTestItem,Diagnosis,Prescription]
mymodels=usermodels+pharmamodels+hospitalmodels

for modelss in mymodels:
    admin.site.register(modelss)