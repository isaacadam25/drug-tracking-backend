from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView,Response
from .serializers import *
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