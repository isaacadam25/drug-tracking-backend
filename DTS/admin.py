from DTS.hub_models import InstituteType
from django.contrib import admin
from .user_models import *
from .transaction_models import *
from .stock_models import *
# Register your models here
hubmodels=[Local,Institute,InstituteType,ExpiredTable,DrugTrackTable]
transactionmodels=[Transaction,TransactionType]
stockmodels=[Batch,MedicineType,Approval,MedicineDetails,Manufacturer]
usermodels=[UserType,UserProfile]

mymodels=usermodels+stockmodels+hubmodels+transactionmodels
for model in mymodels:
    admin.site.register(model)