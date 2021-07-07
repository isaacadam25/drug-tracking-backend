from DTS.hub_models import Institute
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView,Response
from .serializers import *
from DTS.stock_models import Batch,Approval
from DTS.transaction_models import Transaction
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
class MedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=MedicineSerializer
    lookup_url_kwarg = 'id'
    queryset=Medicine.objects.all()

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

class SingleOrderAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=OrderSerializer
    lookup_url_kwarg='id'
    queryset=Order.objects.all()

class RemainingMedicineMSD(APIView):
    pass
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
            msd=Institute.objects.get(reference_number="INS75821246")
            batches=Batch.objects.get(id=stock['id'])
            quantity_list=list()
            used_list=list()
            quantity_list.append(batches.quantity_received)
            used=Transaction.objects.filter(transaction_type__type_name='sales').filter(location_from=msd.id).filter(batch=stock['id'])
            for use in used:
                used_list.append(use.quantity)
            batch_dict[batches.batch_number]=sumofquantities(quantity_list)-sumofquantities(used_list)

        return Response(batch_dict)



