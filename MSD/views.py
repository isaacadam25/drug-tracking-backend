from DTS.hub_models import Institute
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView,Response
from .serializers import *
from DTS.stock_models import Batch,Approval
from DTS.hub_models import Institute
from DTS.transaction_models import Transaction, TransactionType
from rest_framework.permissions import IsAuthenticated, AllowAny
import datetime

# Create your views here.
class MedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=MedicineSerializer
    lookup_url_kwarg = 'id'
    queryset=Medicine.objects.all()

class SendOrderAPI(APIView):
    def patch(self,request,id,format=None):
        transaction_type=TransactionType.objects.get(type_name='sales')
        location_from= Institute.objects.get(name='msd')
        order_to=Order.objects.get(id=id)
        order_items=OrderedItem.objects.filter(order=order_to)
        for order_item in order_items:
            new_trans=Transaction.objects.create(transaction_type=transaction_type,batch=order_item.batch,quantity=order_item.quantity,location_to=order_to.destination,location_from=location_from)
            new_trans.save()
        serializer=ItemSerializer(order_items,many=True)
        return Response(serializer.data)


class MedicineAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Medicine.objects.all()
    serializer_class=MedicineSerializer


class CreateViewOrdersAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Order.objects.all()
    serializer_class=OrderSerializer

class CreateViewOrderItemAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,pk,format=None):
        #order=Order.objects.get(id=pk)
        items=OrderedItem.objects.filter(order=pk)
        serializer=ItemSerializer(items,many=True)
        return Response(serializer.data)


class LatestOrderAPI(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class=OrderSerializer
    # lookup_url_kwarg='date_added'
    queryset=Order.objects.all()
    def get_object(self, *args, **kwargs):
        return self.queryset.latest('order_date')

class OrderItemAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=OrderedItem.objects.all()
    serializer_class=ItemSerializer

class SingleOrderAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=OrderSerializer
    lookup_url_kwarg='id'
    queryset=Order.objects.all()

class RemainingMedicineMSD(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        locations=Transaction.objects.values('location_to').distinct()
        medicine_in=Approval.objects.filter(status=True).filter(id__expiry_date__gt=datetime.date.today()).values('id').distinct()
        medicine_left=Transaction.objects.values('batch').distinct()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        batch_dict=dict()
        for stock in medicine_in:
            msd=Institute.objects.get(name="msd")
            batches=Batch.objects.get(id=stock['id'])
            quantity_list=list()
            used_list=list()
            quantity_list.append(batches.quantity_received)
            used=Transaction.objects.filter(transaction_type__type_name='sales').filter(location_from=msd.id).filter(batch=stock['id'])
            for use in used:
                used_list.append(use.quantity)
            batch_dict[batches.batch_number]=sumofquantities(quantity_list)-sumofquantities(used_list)

        return Response(batch_dict)
# medicine_left=Transaction.objects.filter(batch__expiry_date__lte=datetime.date.today()).values('batch').distinct()
class GetAvailableMSDBAtches(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        locations=Transaction.objects.values('location_to').distinct()
        medicine_in=Approval.objects.filter(status=True).filter(id__expiry_date__gt=datetime.date.today()).values('id').distinct()
        medicine_left=Transaction.objects.values('batch').distinct()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        batch_dict=dict()
        for stock in medicine_in:
            msd=Institute.objects.get(name="msd")
            batches=Batch.objects.get(id=stock['id'])
            quantity_list=list()
            used_list=list()
            quantity_list.append(batches.quantity_received)
            used=Transaction.objects.filter(transaction_type__type_name='sales').filter(location_from=msd.id).filter(batch=stock['id'])
            for use in used:
                used_list.append(use.quantity)
            batch_dict[batches.batch_number]=sumofquantities(quantity_list)-sumofquantities(used_list)

        return Response(batch_dict)

class GetAvailableQuantityMSDBAtches(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        locations=Transaction.objects.values('location_to').distinct()
        medicine_in=Approval.objects.filter(status=True).filter(id__expiry_date__gt=datetime.date.today()).values('id').distinct()
        medicine_left=Transaction.objects.values('batch').distinct()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        batch_dict=dict()
        final_quantity=0
        for stock in medicine_in:
            msd=Institute.objects.get(name="msd")
            batches=Batch.objects.get(id=stock['id'])
            quantity_list=list()
            used_list=list()
            quantity_list.append(batches.quantity_received)
            used=Transaction.objects.filter(transaction_type__type_name='sales').filter(location_from=msd.id).filter(batch=stock['id'])
            
            for use in used:
                used_list.append(use.quantity)
            batch_dict[batches.batch_number]=((sumofquantities(quantity_list)*batches.unit_of_measure)-sumofquantities(used_list))/batches.unit_of_measure
            for quantity in batch_dict.values():
                final_quantity=final_quantity+int(quantity)




        return Response(final_quantity)


class GetExpiredMSDBatches(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        locations=Transaction.objects.values('location_to').distinct()
        medicine_in=Approval.objects.filter(status=True).filter(id__expiry_date__lte=datetime.date.today()).values('id').distinct()
        medicine_left=Transaction.objects.values('batch').distinct()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        batch_dict=dict()
        for stock in medicine_in:
            msd=Institute.objects.get(name="msd")
            batches=Batch.objects.get(id=stock['id'])
            quantity_list=list()
            used_list=list()
            quantity_list.append(batches.quantity_received)
            used=Transaction.objects.filter(transaction_type__type_name='sales').filter(location_from=msd.id).filter(batch=stock['id'])
            for use in used:
                used_list.append(use.quantity)
            batch_dict[batches.batch_number]=sumofquantities(quantity_list)-sumofquantities(used_list)
        quantity=0
        for batch in batch_dict.values():
            quantity=quantity+batch

        return Response(quantity)
    
class GetAllAcceptedBatchesAPI(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        locations=Transaction.objects.values('location_to').distinct()
        medicine_in=Approval.objects.filter(status=True).values('id').distinct()
        medicine_left=Transaction.objects.values('batch').distinct()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        batch_dict=dict()
        for stock in medicine_in:
            msd=Institute.objects.get(name="msd")
            batches=Batch.objects.get(id=stock['id'])
            used_list=list()
            used=Transaction.objects.filter(transaction_type__type_name='sales').filter(location_from=msd.id).filter(batch=stock['id']).filter(is_accepted=True)
            for use in used:
                used_list.append(use.quantity)
            batch_dict[batches.batch_number]=sumofquantities(used_list)
        quantity=0
        for batch in batch_dict.values():
            quantity=quantity+batch

        return Response(quantity)

class GetPendingTransactions(APIView):
    pass

class GetDistributedMedicinesQuantity(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        locations=Transaction.objects.values('location_to').distinct()
        medicine_in=Approval.objects.filter(status=True).values('id').distinct()
        medicine_left=Transaction.objects.values('batch').distinct()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        quantity=0
        batch_dict=dict()
        for stock in medicine_in:
            msd=Institute.objects.get(name="msd")
            batches=Batch.objects.get(id=stock['id'])
            used_list=list()
            used=Transaction.objects.filter(transaction_type__type_name='sales').filter(location_from=msd.id).filter(batch=stock['id'])
            for use in used:
                used_list.append(use.quantity)
            quantity=quantity+(sumofquantities(used_list))
        # quantity=0
        # for batch in batch_dict.values():
        #     quantity=quantity+int(batch)

        return Response(quantity)

class GetDistributedMedicines(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        locations=Transaction.objects.values('location_to').distinct()
        medicine_in=Approval.objects.filter(status=True).values('id').distinct()
        medicine_left=Transaction.objects.values('batch').distinct()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        batch_dict=dict()
        for stock in medicine_in:
            msd=Institute.objects.get(name="msd")
            batches=Batch.objects.get(id=stock['id'])
            used_list=list()
            used=Transaction.objects.filter(transaction_type__type_name='sales').filter(location_from=msd.id).filter(batch=stock['id'])
            for use in used:
                used_list.append(use.quantity)
            batch_dict[batches.batch_number]=sumofquantities(used_list)/batches.unit_of_measure
        quantity=0
        for batch in batch_dict.values():
            quantity=quantity+int(batch)

        return Response(quantity)

    
    



