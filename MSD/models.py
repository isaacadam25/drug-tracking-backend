from django.db import models
from DTS.stock_models import Batch
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