from django.db import models
from DTS.stock_models import Batch
from DTS.hub_models import Institute as Destination
import random
# Create your models here.
class Medicine(models.Model):
    def generate_num():
        serials=[]
        new=list(Medicine.objects.values_list('serial_number'))
        for n in new:
            for l in n:
                serials.append(l)
        not_unique = True
        while not_unique:
            x = f'SN{random.randint(10000000,99999999)}'
            if x not in serials:
                not_unique=False
        return x
    serial_number=models.CharField(max_length=10,blank=True,editable=False,unique=True,default=generate_num)
    quantity=models.IntegerField()
    used=models.IntegerField(blank=True,default=0)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    stock_status=models.CharField(max_length=30,blank=True,null=True)
    batch=models.ForeignKey(Batch, on_delete=models.CASCADE)
    on_route=models.BooleanField(blank=True,default=False)
    def __str__(self):
        return f'{self.serial_number} || {self.batch}'


#################################SALES#####################################
# class OrderType(models.Model):
#     name=models.CharField(max_length=40)
#     description=models.TextField(null=True, blank=True)
#     date_added=models.DateTimeField(auto_now_add=True)
#     date_modified=models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return f'{self.id} {self.name}'

class Order(models.Model):
    def generate_num():
        serials=[]
        new=list(Order.objects.values_list('reference_number'))
        for n in new:
            for l in n:
                serials.append(l)
        not_unique = True
        while not_unique:
            x = random.randint(10000000,99999999)
            if x not in serials:
                not_unique=False
        return x
    reference_number=models.IntegerField(blank=True,editable=False,unique=True,default=generate_num)
    total_quantity=models.IntegerField(blank=True,null=True)
    #order_type=models.ForeignKey(OrderType,null=True,on_delete=models.SET_NULL)
    #order_price=models.FloatField()
    order_date=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(max_length=3,blank=True,default='inc')
    destination=models.ForeignKey(Destination, on_delete=models.PROTECT)
    description=models.TextField(null=True, blank=True)
    def __str__(self):
        return f'{self.id}'

class OrderedItem(models.Model):
    def generate_num():
        serials=[]
        new=list(Order.objects.values_list('item_number'))
        for n in new:
            for l in n:
                serials.append(l)
        not_unique = True
        while not_unique:
            x = random.randint(10000000,99999999)
            if x not in serials:
                not_unique=False
        return x
    item_number=models.IntegerField()
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    description=models.TextField(null=True, blank=True)
    def __str__(self):
        return f'{self.id}'