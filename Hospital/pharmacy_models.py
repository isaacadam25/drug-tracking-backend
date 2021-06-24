from django.db import models
from .user_models import UserProfile as User

# Create your models here.
class MSDZone(models.Model):
    zone_name=models.CharField(max_length=50)
    location=models.CharField(max_length=30)
    description=models.TextField(null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.zone_name}'
    

class MedicineBrand(models.Model):
    brand_name=models.CharField(max_length=50)
    location=models.CharField(max_length=50)
    description=models.TextField(null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.brand_name}'
    

class Batch(models.Model):
    batch_number=models.IntegerField(unique=True)
    medicine_brand=models.ForeignKey(MedicineBrand,on_delete=models.PROTECT)
    measure_options=(('ml','ML'),('cp','CP'),('tb','TB'))
    unit_of_measure = models.CharField(max_length=2, choices=measure_options,default='tb',blank=True)
    quantity_measure=models.IntegerField()
    medicine_name=models.CharField(max_length=30)
    manufacturing_date=models.DateField()
    description=models.TextField(null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.batch_number}-{self.medicine_name}'
   

class Medicine(models.Model):
    serialnumber=models.IntegerField()
    quantity=models.IntegerField()
    # def quantt(self):
    #     quantity_one=self.batch.quantity_of_measure
    #     x=self.quantity*quantity_one
    #     return x
    batch=models.ForeignKey(Batch, on_delete=models.CASCADE)
    t_quantity=models.IntegerField()
    tq_used=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=30)
    price=models.FloatField()
    description=models.TextField(null=True, blank=True)
    batch=models.ForeignKey(Batch, on_delete=models.CASCADE)
    msd_zone=models.ForeignKey(MSDZone, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.id}'
   

class Supplier(models.Model):
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=50)
    contacts=models.CharField(max_length=15)
    def __str__(self):
        return f'{self.name}'







    