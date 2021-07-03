from django.shortcuts import render
from rest_framework import status,generics, request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
# from MSD.models import MSDMedicine
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.db.models import Q
from rest_framework.response import Response
import datetime
from DTS.hub_models import *
from DTS.user_models import *
from DTS.stock_models import *
from DTS.transaction_models import *
from DTS.hub_serializers import *
from DTS.stock_serializers import *
from DTS.transaction_serializers import *
from DTS.user_serializers import *


class TopApprovedMedicine(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        names=MedicineDetails.objects.values('name').distinct()
        content=dict()
        for name in names:
            count=Approval.objects.filter(status=True).filter(id__medicine_detail__name=name['name']).count()
            content[name['name']]=count
        sort=sorted(content.items(), key=lambda x:x[1], reverse=True)
        return Response(dict(sort))

class TopApprovedManufacturersAPI(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        manufacturers=MedicineDetails.objects.values('manufacturer').distinct()
        content=dict()
        for manufacturer in manufacturers:
            count=Approval.objects.filter(status=True).filter(id__medicine_detail__manufacturer=manufacturer['manufacturer']).count()
            content[manufacturer['manufacturer']]=count
        sort=sorted(content.items(), key=lambda x:x[1], reverse=True)
        return Response(dict(sort))   

class TopDeclinedManufacturersAPI(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        manufacturers=MedicineDetails.objects.values('manufacturer').distinct()
        content=dict()
        for manufacturer in manufacturers:
            count=Approval.objects.filter(is_declined=True).filter(id__medicine_detail__manufacturer=manufacturer['manufacturer']).count()
            content[manufacturer['manufacturer']]=count
        sort=sorted(content.items(), key=lambda x:x[1], reverse=True)
        return Response(dict(sort))   
    
class GetRemainingMedicineHospital(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        locations=Transaction.objects.values('location_to').distinct()
        medicine=Transaction.objects.values('batch').distinct()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        institutes=dict()
        for institute in locations:
            batch_dict=dict()
            for batches in medicine:
                stock=Transaction.objects.filter(location_to=institute['location_to']).filter(batch=batches['batch']).filter(transaction_type__type_name='purchase')
                used=Transaction.objects.filter(is_accepted=True).filter(location_from=institute['location_to']).filter(location_to=institute['location_to']).filter(batch=batches['batch']).filter(transaction_type__type_name='sales')
                quantity_list=list()
                used_list=list()
                for seen in stock:
                    quantity_list.append(seen.quantity)
                for use in used:
                    used_list.append(use.quantity)
                newvar=Batch.objects.get(id=batches['batch'])
                batch_dict[newvar.batch_number]=(sumofquantities(quantity_list)*newvar.unit_of_measure)-sumofquantities(used_list)
            newisnt=Institute.objects.get(id=institute['location_to'])
            institutes[newisnt.reference_number]=batch_dict
        #sort=sorted(content.items(), key=lambda x:x[1], reverse=True)
        return Response(institutes)   
        