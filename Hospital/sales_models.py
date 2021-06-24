from django.db import models
from .pharmacy_models import Supplier, Medicine
from .hospital_models import Patient

class OrderType(models.Model):
    name=models.CharField(max_length=40)
    description=models.TextField(null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.id}'

class Order(models.Model):
    reference_number=models.IntegerField()
    supplier=models.ForeignKey(Supplier, models.PROTECT)
    total_quantity=models.IntegerField()
    order_type=models.ForeignKey(OrderType,null=True,on_delete=models.SET_NULL)
    order_price=models.FloatField()
    order_date=models.DateTimeField()
    order_status=models.CharField(max_length=3)
    description=models.TextField(null=True, blank=True)
    def __str__(self):
        return f'{self.id}'

class OrderedItem(models.Model):
    medicine=models.ForeignKey(Medicine,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    description=models.TextField(null=True, blank=True)
    def __str__(self):
        return f'{self.id}'


class Invoice(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    date_on_invoice=models.DateTimeField(auto_now_add=True)
    total_price=models.FloatField()
    status=models.CharField(max_length=30)
    description=models.TextField(null=True, blank=True)
    def __str__(self):
        return f'{self.id}'

class Transaction(models.Model):
    reference_number=models.IntegerField(unique=True)
    date_issued=models.DateTimeField(auto_now_add=True)
    description=models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.reference_number}"

class AppointmentFee(models.Model):
    amount=models.IntegerField()
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    is_paid=models.BooleanField(default=False)
    transaction=models.ForeignKey(Transaction,on_delete=models.PROTECT)
    description=models.TextField(null=True, blank=True)


