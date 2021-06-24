from Hospital.pharmacy_serializers import MedicineSerializer
from django.contrib import admin
from .user_models import *
from .pharmacy_models import *
from .hospital_models import *
from .sales_models import *
# Register your models here.
usermodels=[UserProfile,UserType,HospitalRoom]
salesmodels=[Order,Transaction,OrderType,OrderedItem,Invoice,AppointmentFee]
pharmamodels=[MedicineBrand,Batch,Medicine,MSDZone,Supplier]
hospitalmodels=[Patient,PatientType,Appointment,Labtest,LabTestItem,Diagnosis]
mymodels=usermodels+pharmamodels+hospitalmodels
for model in mymodels:
    admin.site.register(model)