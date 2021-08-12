from django.db import models
from django.db.models.deletion import DO_NOTHING
from .user_models import UserProfile as User

# Create your models here.
# class MSDZone(models.Model):
#     zone_name=models.CharField(max_length=50)
#     zone_location=models.CharField(max_length=30)
#     description=models.TextField()
#     date_added=models.DateTimeField(auto_now_add=True)
#     date_modified=models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return f'{self.zone_name}'
    

# class MedicineBrand(models.Model):
#     brand_name=models.CharField(max_length=50)
#     location=models.CharField(max_length=50)
#     description=models.TextField()
#     date_added=models.DateTimeField(auto_now_add=True)
#     date_modified=models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return f'{self.brand_name}'

class Manufacturer(models.Model):
    name=models.CharField(max_length=30,unique=True)
    nation=models.CharField(max_length=30)
    is_active=models.BooleanField(default=True)
    description=models.TextField(blank=True,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True) 
    def __str__(self):
        return f'{self.name}'

class MedicineDetails(models.Model):
    name=models.CharField(max_length=30)
    manufacturer=models.ForeignKey(Manufacturer,on_delete=models.CASCADE)
    description=models.TextField(blank=True,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.manufacturer} {self.name}'
    

class MedicineType(models.Model):
    type_name=models.CharField(max_length=30)
    description=models.TextField(blank=True,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.type_name}'


class Batch(models.Model):
    medicine_detail=models.ForeignKey(MedicineDetails,on_delete=DO_NOTHING)
    batch_number=models.IntegerField()
    used=models.IntegerField(default=0)
    quantity_received=models.IntegerField()
    unit_of_measure = models.IntegerField(default=100)
    concentration=models.CharField(max_length=15)
    description=models.TextField(blank=True,null=True)
    production_date=models.DateField()
    expiry_date=models.DateField()
    medicine_type=models.ForeignKey(MedicineType, on_delete=models.SET_NULL,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):
        super(Batch,self).save(*args,**kwargs)
        approve=Approval()
        approve.id=self
        approve.save()

    def __str__(self):
        return f'{self.batch_number} || {self.medicine_detail}'

class Approval(models.Model):
    id=models.OneToOneField(Batch,on_delete=models.CASCADE,unique=True,primary_key=True)
    #approver=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    status=models.BooleanField(default=False,blank=True)
    is_declined=models.BooleanField(default=False,blank=True)
    date_approved=models.DateField(null=True,blank=True)
    description=models.TextField(blank=True,null=True)
    def status_check(self):
        if self.is_declined:
            return f'Declined'
        if self.status:
            return f'Approved'
        return f'Unapproved'
    def __str__(self):
        if self.is_declined:
            return f'{self.id.batch_number} || Declined'
        if self.status:
            return f'{self.id.batch_number} || Approved'
        return f'{self.id.batch_number} || Unapproved'



# class Supplier(models.Model):
#     name=models.CharField(max_length=30)
#     address=models.CharField(max_length=50)
#     contacts=models.CharField(max_length=15)
#     def __str__(self):
#         return f'{self.name}'







    
