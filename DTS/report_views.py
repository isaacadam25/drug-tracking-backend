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
from django.db.models import F



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

class GetRemainingMedicineSingleHospital(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request,refno):
        institute=Institute.objects.get(reference_number=refno)
        medicine=Transaction.objects.values('batch').distinct()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        batch_dict=dict()
        for batches in medicine:
            stock=Transaction.objects.filter(location_to=institute).filter(batch=batches['batch']).filter(transaction_type__type_name='purchase')
            used=Transaction.objects.filter(is_accepted=True).filter(location_from=institute).filter(location_to=institute).filter(batch=batches['batch']).filter(transaction_type__type_name='sales')
            quantity_list=list()
            used_list=list()
            for seen in stock:
                quantity_list.append(seen.quantity)
            for use in used:
                used_list.append(use.quantity)
            newvar=Batch.objects.get(id=batches['batch'])
            batch_dict[newvar.batch_number]=(sumofquantities(quantity_list)*newvar.unit_of_measure)-sumofquantities(used_list)
         #sort=sorted(content.items(), key=lambda x:x[1], reverse=True)
        return Response(batch_dict)

class GetRemainingMedicineSingleHospitalQuantity(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request,refno):
        institute=Institute.objects.get(reference_number=refno)
        medicine=Transaction.objects.values('batch').distinct()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        batch_dict=dict()
        for batches in medicine:
            stock=Transaction.objects.filter(location_to=institute).filter(batch=batches['batch']).filter(transaction_type__type_name='purchase')
            used=Transaction.objects.filter(is_accepted=True).filter(location_from=institute).filter(location_to=institute).filter(batch=batches['batch']).filter(transaction_type__type_name='sales')
            quantity_list=list()
            used_list=list()
            for seen in stock:
                quantity_list.append(seen.quantity)
            for use in used:
                used_list.append(use.quantity)
            newvar=Batch.objects.get(id=batches['batch'])
            batch_dict[newvar.batch_number]=((sumofquantities(quantity_list)*newvar.unit_of_measure)-sumofquantities(used_list))/newvar.unit_of_measure
        amount=0
        for quantities in batch_dict.values():
            amount=amount+quantities
        content={'Available':int(amount)}
         #sort=sorted(content.items(), key=lambda x:x[1], reverse=True)
        return Response(content)

class GetExpiredMedicineSingleHospitalQuantity(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request,refno):
        institute=Institute.objects.get(reference_number=refno)
        medicine=Transaction.objects.filter(batch__expiry_date__lte=datetime.date.today()).values('batch').distinct()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        batch_dict=dict()
        for batches in medicine:
            stock=Transaction.objects.filter(location_to=institute).filter(batch=batches['batch']).filter(transaction_type__type_name='purchase')
            used=Transaction.objects.filter(is_accepted=True).filter(location_from=institute).filter(location_to=institute).filter(batch=batches['batch']).filter(transaction_type__type_name='sales')
            quantity_list=list()
            used_list=list()
            for seen in stock:
                quantity_list.append(seen.quantity)
            for use in used:
                used_list.append(use.quantity)
            newvar=Batch.objects.get(id=batches['batch'])
            batch_dict[newvar.batch_number]=((sumofquantities(quantity_list)*newvar.unit_of_measure)-sumofquantities(used_list))/newvar.unit_of_measure
        amount=0
        for quantities in batch_dict.values():
            amount=amount+quantities
        content={'Available':int(amount)}
         #sort=sorted(content.items(), key=lambda x:x[1], reverse=True)
        return Response(content)
class GetReceivedMedicineQuantity(APIView):
    def get(self,request,refno):
        medicine=Transaction.objects.filter(location_to__reference_number=refno).values('batch').distinct()
        batch_dict=dict()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        for batches in medicine:
            stock=Transaction.objects.filter(location_to__reference_number=refno).filter(batch=batches['batch']).filter(transaction_type__type_name='purchase')
            quantity_list=list()
            for seen in stock:
                quantity_list.append(seen.quantity)
            newvar=Batch.objects.get(id=batches['batch'])
            batch_dict[newvar.batch_number]=sumofquantities(quantity_list)
        amount=0
        for quantities in batch_dict.values():
            amount=amount+quantities
        content={'Received':int(amount)}
        return Response(content)


# class GetAllDrugsFromHospital(APIView):
#     permission_classes=(IsAuthenticated,)
#     def get(self,request,rno):
#         batches=Transaction.objects.filter(transaction_type__type_name='purchase').filter(location_to=rno).values('batch').distinct()
#         #all_drugs_entered=Transaction.objects.filter(transaction_type__type_name='purchase').filter(location_to=rno).values('batch').distinct()
#         hospital_batches=dict()
#         for batch in batches:
#             val=Batch.objects.get(id=batch['batch'])
            
#             hospital_batches[val.batch_number]=val


        
#         pass

class GetBatchLost(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):

        #batches=Transaction.objects.filter(transaction_type__type_name='sales').filter(is_accepted=False).filter(location_to=F(~Q('location_from')))
        batches=Transaction.objects.filter(transaction_type__type_name='sales').filter(is_accepted=False).filter(~Q(location_to=F('location_from'))).filter(date_added__lte=(datetime.date.today()-datetime.timedelta(days=3)))
        output=TransactionSerializer(batches,many=True)
        return Response(output.data)
class GetBatchLostFromMSD(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        #transaction to
        sent=Transaction.objects.filter(transaction_type__type_name='sales').filter(is_accepted=True).filter(~Q(location_to=F('location_from')))
        #purchase_transaction
        lost=dict()
        for s in sent:
            lost_item=dict()
            received=Transaction.objects.get(corresponding_transaction=s.reference_number)
            if s.quantity != received.quantity:
                lost_item['unit_quantity_lost'] = (s.quantity-received.quantity)*s.batch.unit_of_measure
                #lost_item['sent_reference_number'] = 
                lost_item['quantity_lost'] = (s.quantity-received.quantity)
                lost_item['acceptor_fname'] = received.initiator.actual_user.first_name
                lost_item['acceptor_lname'] = received.initiator.actual_user.last_name
                lost_item['acceptor_organization'] = received.initiator.organization.name
                lost_item['receiver_region'] = received.initiator.organization.location.region
                lost_item['receiver_city'] = received.initiator.organization.location.city
                lost_item['sender_fname']=s.initiator.actual_user.first_name
                lost_item['sender_lname']=s.initiator.actual_user.last_name
                lost_item['sender_organization']=s.initiator.organization.name
                lost_item['sender_region']=s.initiator.organization.location.region
                lost_item['sender_city']=s.initiator.organization.location.city
                lost[s.reference_number]=lost_item

        return Response(lost)

class BatchTrace(APIView):
    def get(self,request,id):
        traces=Transaction.objects.filter(transaction_type__type_name='purchase').filter(batch=id)
        #initial location
        msd=Approval.objects.get(id=id)
        val1=Institute.objects.get(name='msd') 
        time_location=dict()
        time_location[val1.name]= msd.date_approved
        #all other following locations
        for local in traces:
           #location_track=Transaction.objects.filter(location_to=local).order_by('date_added')
           val=Institute.objects.get(id=local.location_to.id)
           time_location[val.name]=local.date_added
        return Response(time_location)

class BatchTrack(APIView):
    def get(self,request,id):
        location=Transaction.objects.filter(transaction_type__type_name='sales').filter(batch=id).values('location_to')
        all=Transaction.objects.filter(transaction_type__type_name='sales')
       #for al l
        latest=location.latest('date_added')
        pass

#DestroyExpiredDrugs
class GetDrugsNeedDestroying(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request,refno):
        institute=Institute.objects.get(reference_number=refno)
        expiry_table=ExpiredTable.objects.filter(organization=institute).order_by('destruction_date')
        if len(expiry_table) == 0:
            medicine=Transaction.objects.filter(batch__expiry_date__lte=datetime.date.today()).values('batch').distinct()
        else:
            destroy_date=expiry_table[len(expiry_table)-1].destruction_date
            medicine=Transaction.objects.filter(batch__expiry_date__lte=datetime.date.today()).filter(batch__expiry_date__gt=destroy_date).values('batch').distinct()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        batch_dict=dict()
        for batches in medicine:
            stock=Transaction.objects.filter(location_to=institute).filter(batch=batches['batch']).filter(transaction_type__type_name='purchase')
            used=Transaction.objects.filter(is_accepted=True).filter(location_from=institute).filter(location_to=institute).filter(batch=batches['batch']).filter(transaction_type__type_name='sales')
            quantity_list=list()
            used_list=list()
            for seen in stock:
                quantity_list.append(seen.quantity)
            for use in used:
                used_list.append(use.quantity)
            newvar=Batch.objects.get(id=batches['batch'])
            batch_dict[newvar.batch_number]=((sumofquantities(quantity_list)*newvar.unit_of_measure)-sumofquantities(used_list))/newvar.unit_of_measure
        amount=0
        for quantities in batch_dict.values():
            amount=amount+quantities
        content={'Expired':int(amount)}
         #sort=sorted(content.items(), key=lambda x:x[1], reverse=True)
        return Response(amount)

class CreateExpireTableInstance(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=ExpiredTable.objects.all()
    serializer_class=ExpiredTableSerializer


class GetMostExpiredMedicines(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        months_name=['January','February','March','April','May','June','July','August','September','October','November','December']
        month_dig=[1,2,3,4,5,6,7,8,9,10,11,12,13]
        year_now=datetime.datetime.now().year
        medicine_name=MedicineDetails.objects.values('name').distinct()
        batch_list=list()
        batch=Transaction.objects.filter(batch__expiry_date__lte=datetime.date.today()).values('batch').distinct()
        medicine_name_dict=dict()
        for b in batch:
            batch_list.append(b['batch'])
        name_medicine=dict()
        for name in medicine_name:
            batch_quantity=0
            transaction_batches=Batch.objects.filter(medicine_detail__name=name).filter(id__in=batch_list)
            for t_batches in transaction_batches:
                name_quantity=0
                name_used=0
                stock=Transaction.objects.filter(batch=t_batches).filter(transaction_type__type_name='purchase')
                used=Transaction.objects.filter(is_accepted=True).filter(location_to=F('location_from')).filter(batch=t_batches).filter(transaction_type__type_name='sales')
                
                for seen in stock:
                    name_quantity=name_quantity+seen.quantity
                for use in used:
                    name_used=name_used+use.quantity
                newvar=Batch.objects.get(id=t_batches.id)
                batch_quantity=batch_quantity+(name_quantity*newvar.unit_of_measure)-name_used/newvar.unit_of_measure
                
            name_medicine[name['name']]=batch_quantity

        return Response(name_medicine)

class GetExpireTrend(APIView):
    def get(self,request):
        months_name=['January','February','March','April','May','June','July','August','September','October','November','December']
        month_dig=[1,2,3,4,5,6,7,8,9,10,11,12,13]
        year_now=datetime.datetime.now().year
        medicine_name=MedicineDetails.objects.values('name').distinct()
        batch_list=list()
        batch=Transaction.objects.filter(batch__expiry_date__lte=datetime.date.today()).values('batch').distinct()
        medicine_name_dict=dict()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        for b in batch:
            batch_list.append(b['batch'])
        batch_dict=dict()
        for name in medicine_name:
            transaction_batches=Batch.objects.filter(medicine_detail__name=name).filter(id__in=batch_list)

            for batches in transaction_batches:
                med=Approval.objects.get(id=batches['batch'])
            
                stock=Transaction.objects.filter(batch=batches).filter(transaction_type__type_name='purchase')
                used=Transaction.objects.filter(is_accepted=True).filter(location_to=F('location_from')).filter(batch=batches).filter(transaction_type__type_name='sales')
                quantity_list=list()
                used_list=list()
                for seen in stock:
                    quantity_list.append(seen.quantity)
                for use in used:
                    used_list.append(use.quantity)
                newvar=Batch.objects.get(id=batches['batch'])
                batch_dict[newvar.medicine_detail]=((sumofquantities(quantity_list)*newvar.unit_of_measure)-sumofquantities(used_list))/newvar.unit_of_measure
        amount=0
        for quantities in batch_dict.values():
            amount=amount+quantities
        content={'Expired':int(amount)}
            #sort=sorted(content.items(), key=lambda x:x[1], reverse=True)
        return Response(content)

class MedicineUsedPieChartAPI(APIView):
    def get(self,request,batchid):
        institutes=Institute.objects.filter(~Q(institute_type__name="ministry")).filter(~Q(institute_type__name="tmda")).filter(~Q(institute_type__name="msd")).filter(~Q(institute_type__name="moh")).filter(~Q(institute_type__name="government")).values('reference_number')
        newlist=list()
        for org in institutes:
            institute_dict=dict()
            institute=Institute.objects.get(reference_number=org['reference_number'])
            def sumofquantities(arr):
                sum=0
                for values in arr:
                    sum=sum+values
                return sum
            
            used=Transaction.objects.filter(is_accepted=True).filter(location_from=institute).filter(location_to=F('location_from')).filter(batch=batchid).filter(transaction_type__type_name='sales')
            
            used_list=list()
            for use in used:
                used_list.append(use.quantity)
            newvar=Batch.objects.get(id=batchid)
            amount=0
            for quantities in used_list:
                amount=amount+quantities
            institute_dict['institute']=institute.name
            institute_dict['quantity']=int(amount)
            newlist.append(institute_dict)
        return Response(newlist)

class MostUsedBatches(APIView):
    def get(self,request):
        medicine=Transaction.objects.filter(location_to=F('location_from')).values('batch').distinct()
        
        listnew=list()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        for batches in medicine:
            batch_dict=dict()
            used=Transaction.objects.filter(batch=batches['batch']).filter(transaction_type__type_name='sales')
            quantity_list=list()
            for seen in used:
                quantity_list.append(seen.quantity)
            newvar=Batch.objects.get(id=batches['batch'])
            batch_dict['id']=newvar.id
            batch_dict['batch_number']=newvar.batch_number
            batch_dict['quantity']=sumofquantities(quantity_list)
            batch_dict['medicine_name']=newvar.medicine_detail.name
            listnew.append(batch_dict)
        

        return Response(listnew)