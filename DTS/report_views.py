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
from math import ceil



class TopApprovedMedicine(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        names=MedicineDetails.objects.values('name').distinct()
        content_list=list()
        for name in names:
            content=dict()
            count=Approval.objects.filter(status=True).filter(id__medicine_detail__name=name['name']).count()
            content['medicine']=name['name']
            content['batches']=count
            content_list.append(content)
        sort=sorted(content_list, key=lambda x:x['batches'], reverse=True)
        return Response(sort)

class TopApprovedManufacturersAPI(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        manufacturers=MedicineDetails.objects.values('manufacturer').distinct()
        content_list=list()
        for manufacturer in manufacturers:
            content=dict()
            count=Approval.objects.filter(status=True).filter(id__medicine_detail__manufacturer=manufacturer['manufacturer']).count()
            manufacturer_instance=Manufacturer.objects.get(id=manufacturer['manufacturer'])
            content['manufacturer']=manufacturer_instance.name
            content['quantity']=count
            content_list.append(content)
        sort=sorted(content_list, key=lambda x:x['quantity'], reverse=True)
        return Response(sort)   

class TopDeclinedManufacturersAPI(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        manufacturers=MedicineDetails.objects.values('manufacturer').distinct()
        content_list=list()
        
        for manufacturer in manufacturers:
            content=dict()
            count=Approval.objects.filter(is_declined=True).filter(id__medicine_detail__manufacturer=manufacturer['manufacturer']).count()
            content['manufacturer']=manufacturer['manufacturer']
            content['quantity']=count
            content_list.append(content)
        sort=sorted(content_list, key=lambda x:x['quantity'], reverse=True)
        return Response(sort)    
    
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

class GetPercentageOfExpiredUsed(APIView):
    def get(self,request):
        date_last_year=datetime.datetime.now() - datetime.timedelta(days=365)
        medicine=Transaction.objects.filter(batch__expiry_date__lte=datetime.date.today()).filter(batch__expiry_date__gt=date_last_year).values('batch').distinct()
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        batch_list=list()
        for batches in medicine:
            batch_dict=dict()
            stock=Approval.objects.get(id=batches['batch'])
            used=Transaction.objects.filter(is_accepted=True).filter(location_to=F('location_from')).filter(batch=batches['batch']).filter(transaction_type__type_name='sales')

            quantity_list=list()
            used_list=list()
            quantity_of_med=stock.id.quantity_received
            for use in used:
                used_list.append(use.quantity)
            newvar=Batch.objects.get(id=batches['batch'])

            batch_dict['medicine_name']=stock.id.medicine_detail.name
            batch_dict['batch_number']=stock.id.batch_number
            batch_dict['expiry_date']=stock.id.expiry_date
            batch_dict['used']=round((sumofquantities(used_list)*100)/(quantity_of_med*stock.id.unit_of_measure))
            batch_list.append(batch_dict)
        
         #sort=sorted(content.items(), key=lambda x:x[1], reverse=True)
        return Response(batch_list)

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
        sent=Transaction.objects.filter(transaction_type__type_name='sales').filter(is_accepted=True).filter(~Q(location_to=F('location_from'))).order_by("date_added")
        #purchase_transaction
        lost=list()
        for s in sent:
            lost_item=dict()
            received=Transaction.objects.get(corresponding_transaction=s.reference_number)
            if s.quantity != received.quantity:
                lost_item['reference_number']=received.corresponding_transaction
                lost_item['unit_quantity_required'] = (s.quantity)*s.batch.unit_of_measure
                lost_item['unit_quantity_lost'] = (s.quantity-received.quantity)*s.batch.unit_of_measure
                #lost_item['sent_reference_number'] = 
                lost_item['quantity_required'] = (s.quantity)
                lost_item['quantity_lost'] = (s.quantity-received.quantity)
                lost_item['acceptor_fname'] = received.initiator.actual_user.first_name
                lost_item['acceptor_lname'] = received.initiator.actual_user.last_name
                lost_item['acceptor_organization'] = received.initiator.organization.name
                lost_item['receiver_region'] = received.initiator.organization.location.region
                lost_item['receiver_city'] = received.initiator.organization.location.city
                lost_item['date_received']=received.date_added
                lost_item['sender_fname']=s.initiator.actual_user.first_name
                lost_item['sender_lname']=s.initiator.actual_user.last_name
                lost_item['sender_organization']=s.initiator.organization.name
                lost_item['sender_region']=s.initiator.organization.location.region
                lost_item['sender_city']=s.initiator.organization.location.city
                lost_item['date_sent']=s.date_added
                lost.append(lost_item)

        return Response(lost)

class BatchTrace(APIView):
    permission_classes=(AllowAny,)
    def get(self,request,batchno):
        traces=Transaction.objects.filter(transaction_type__type_name='purchase').filter(batch__batch_number=batchno)
        #initial location
        msd=Approval.objects.get(id__batch_number=batchno)
        val1=Institute.objects.get(name='msd') 
        time_location=dict()
        time_location['location']= val1.name
        time_location['date']= msd.date_approved
        batch_list=list()
        batch_list.append(time_location)
        #all other following locations
        for local in traces:
            time_location=dict()
           #location_track=Transaction.objects.filter(location_to=local).order_by('date_added')
            val=Institute.objects.get(id=local.location_to.id)
            time_location['location']=val.name
            time_location['date']=local.date_added
            batch_list.append(time_location)
        return Response(batch_list)

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
        batch_arr=list()
        amount_list=list()
        for batches in medicine:
            batch_dict=dict()
            stock=Transaction.objects.filter(location_to=institute).filter(batch=batches['batch']).filter(transaction_type__type_name='purchase')
            used=Transaction.objects.filter(is_accepted=True).filter(location_from=institute).filter(location_to=institute).filter(batch=batches['batch']).filter(transaction_type__type_name='sales')
            quantity_list=list()
            used_list=list()
            for seen in stock:
                quantity_list.append(seen.quantity)
            for use in used:
                used_list.append(use.quantity)
            newvar=Batch.objects.get(id=batches['batch'])
            batch_dict["batch_number"]=newvar.batch_number
            batch_dict["batch_number"]=newvar.batch_number
            batch_dict["expired_quantity"]=ceil(((sumofquantities(quantity_list)*newvar.unit_of_measure)-sumofquantities(used_list))/newvar.unit_of_measure)
            batch_dict["expired_unit_quantity"]=((sumofquantities(quantity_list)*newvar.unit_of_measure)-sumofquantities(used_list))
            batch_dict["unit_measure"]=newvar.medicine_type.type_name
            batch_arr.append(batch_dict)
            amount=0
            amount_list.append(batch_dict["expired_quantity"])

        
        # batch_arr.append(sumofquantities(amount_list))
        
         #sort=sorted(content.items(), key=lambda x:x[1], reverse=True)
        return Response(batch_arr)

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
        
        for name in medicine_name:
            name_medicine=dict()
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
            name_medicine[name['name']]=batch_quantity

        return Response(name_medicine)


class ExpireTrends(APIView):
    def get(self,request,year):
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        month_dig=ExpiredTable.objects.filter(destruction_date__year=year).values('destruction_date__month').order_by('destruction_date').distinct()
        month_list=list()
        for b in month_dig:
            month_list.append(b['destruction_date__month'])
        j=100
        i=len(month_list)-1
        drug='PARACETAMOL'
        data=list()
        if bool(month_list):
            while(j!=0):
                
                if (i==0):
                    batches=Approval.objects.filter(status=True).filter(id__expiry_date__month__lte=month_list[i]).filter(id__medicine_detail__name=drug).values('id').distinct()
                    j=0
                    # if not bool(batches):
                    #     continue
                else:
                    batches=Approval.objects.filter(status=True).filter(id__expiry_date__month__lte=month_list[i]).filter(id__expiry_date__month__gt=month_list[i-1]).values('id').distinct()
                    i=i-1
                    # if not bool(batches):
                    #     continue
                batch_quant=list()  
                
                
                for batch in batches:
                    med=Batch.objects.get(id=batch['id'])
                    stock=Transaction.objects.filter(batch=med).filter(transaction_type__type_name='purchase')
                    used=Transaction.objects.filter(is_accepted=True).filter(location_to=F('location_from')).filter(batch=med).filter(transaction_type__type_name='sales')
                    quantity_list=list()
                    used_list=list()
                    for seen in stock:
                        quantity_list.append(seen.quantity)
                    
                    for use in used:
                        used_list.append(use.quantity)
                    # newvar=Batch.objects.get(id=batch['batch'])
                    # batch_quant.append(((sumofquantities(quantity_list)*med.unit_of_measure)-sumofquantities(used_list))/med.unit_of_measure)
                    batch_quant.append(((med.quantity_received*med.unit_of_measure)-sumofquantities(used_list))/med.unit_of_measure)
                amount=0
                for quantities in batch_quant:
                    amount=amount+quantities
                data.append(amount)
            content=[{'label':drug,'data':data}]
                #sort=sorted(content.items(), key=lambda x:x[1], reverse=True)
            return Response(content)
        else:
            content={"detail":"No Medicine have been Destroyed this year"}
            return Response(content)



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

class ExpireTrendsone(APIView):
    def get(self,request,year):
        months=[1,2,3,4,5,6,7,8,9,10,11,12]
        month_dig=ExpiredTable.objects.filter(destruction_date__year=year)
        month_list=list()
        j=100
        i=len(month_list)-1
        drug='PARACETAMOL'
        month=1
        data=list()
        batches=Approval.objects.filter(status=True).filter(id__expiry_date__month__lte=month).filter(id__medicine_detail__name=drug).values('id').distinct()
         
        batch_quant=list()  
                
                
        for batch in batches:
            med=Batch.objects.get(id=batch['id'])
            stock=Transaction.objects.filter(batch=med).filter(transaction_type__type_name='purchase')
            used=Transaction.objects.filter(is_accepted=True).filter(location_to=F('location_from')).filter(batch=med).filter(transaction_type__type_name='sales')
            quantity_list=list()
                
        pass
    pass

class ExpireTrends(APIView):
    def get(self,request,year):
        def sumofquantities(arr):
            sum=0
            for values in arr:
                sum=sum+values
            return sum
        month_list=[1,2,3,4,5,6,7,8,9,10,11,12]
        months_name=['January','February','March','April','May','June','July','August','September','October','November','December']
        
        j=100
        i=len(month_list)-1
        get_meds_though_batches=Approval.objects.filter(status=True).filter(id__expiry_date__year=year)
        medname_list=list()
        for b in get_meds_though_batches:
            l=Batch.objects.get(id=b.id.id)
            medname_list.append(l.medicine_detail.name)
        medname_set=set(medname_list)
        data=list()
        d_list=list()
        for drug in medname_set:
            drug_dict=dict()
            for m in month_list:
                
                batches=Approval.objects.filter(status=True).filter(id__expiry_date__month=m).filter(id__medicine_detail__name=drug)
                
                batch_quant_dict=dict() 
                batch_quant_list=list() 
                
                for batch in batches:
                    med=Batch.objects.get(id=batch.id.id)
                    stock=Transaction.objects.filter(batch=med).filter(transaction_type__type_name='purchase')
                    used=Transaction.objects.filter(is_accepted=True).filter(location_to=F('location_from')).filter(batch=med.id).filter(transaction_type__type_name='sales')
                    quantity_list=list()
                    used_list=list()
                    for seen in stock:
                        quantity_list.append(seen.quantity)
                    
                    for use in used:
                        used_list.append(use.quantity)
                    # newvar=Batch.objects.get(id=batch['batch'])
                    # batch_quant.append(((sumofquantities(quantity_list)*med.unit_of_measure)-sumofquantities(used_list))/med.unit_of_measure)
                    batch_quant_list.append(((med.quantity_received*med.unit_of_measure)-sumofquantities(used_list)))
                amount=0
                for quantities in batch_quant_list:
                    amount=amount+quantities
                data.append(amount)
            drug_dict['label']=drug
            drug_dict['data']=data
            d_list.append(drug_dict)
        return Response(d_list)


########################### MOH SYSTEM #################################3

class TransactionLog(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    queryset=Transaction.objects.all().order_by('date_added')   
    serializer_class=TransactionSerializer

class BatchDistribution(APIView):
    permission_classes = (AllowAny,)
    def get(self,request,batchno):
        locations=Transaction.objects.values('location_to__name')
        locations_list=list()
        for local in locations:
            locations_list.append(local['location_to__name'])
        location_set=set(locations_list)
        location_list=list()
        for location in location_set:
            batch_dict=dict()
            amount=0
            transactions=Transaction.objects.filter(location_from__name='msd').filter(location_to__name=location).filter(~Q(location_to=F('location_from'))).filter(transaction_type__type_name='sales')
            for transaction in transactions:
                amount+=transaction.quantity
            batch_dict['location']=location
            batch_dict['amount']=amount
            location_list.append(batch_dict)
        return Response(location_list)

class AllUsedDrugs(APIView):
    def get(self,request):
        transactions=Transaction.objects.filter(location_to=F('location_from')).filter(transaction_type__type_name='sales')
        amount=0
        for t in transactions:
            amount+=t.quantity
        return Response({"amount":amount})

class AllReceivedDrugs(APIView):
    def get(self,request):
        now = datetime.datetime.now()
        year=now.year
        drugs=Approval.objects.filter(date_approved__year=year).filter(status=True)
        amount=0
        for drug in drugs:
            amount+=(drug.id.quantity_received)*drug.id.unit_of_measure
        return Response({'amount':amount})
class AllLostDrugs(APIView):
    def get(self,request):
        date=datetime.datetime.now()
        year=date.year
        sent=Transaction.objects.filter(date_added__year=year).filter(transaction_type__type_name='sales').filter(is_accepted=True).filter(~Q(location_to=F('location_from'))).order_by("date_added")
        #purchase_transaction
        lost=list()
        amount=0
        for s in sent:
            lost_item=dict()
            received=Transaction.objects.get(corresponding_transaction=s.reference_number)
            if s.quantity != received.quantity:
                amount+=(s.quantity-received.quantity)*s.batch.unit_of_measure
        return Response({"amount":amount})


# class AllExpiredDrugs(APIView):
#     def get(self,request):
        
#     pass


class DrugTrackTableAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=DrugTrackTable.objects.all()
    serializer_class=DrugTrackTableSerializer

class GetMissingHospitalDrugs(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=DrugTrackTable.objects.filter(~Q(quantity_destroyed=F("destroyed__quantity_destroyed")))
    serializer_class=DrugTrackTableSerializer

class DestroyAPI(APIView):
    def post(self,request):
        quantity_destroyed=request.data['quantity_destroyed']
        quantity_need=request.data['quantity_needed']
        organization_id=request.data['organization']
        destroyer=request.data['user']
        user=User.objects.get(id=destroyer)
        org=Institute.objects.get(id=organization_id)
        expiry_table=ExpiredTable.objects.create(organization=org,quantity_destroyed=quantity_destroyed)
        expiry_table.save()
        
        drug_track=DrugTrackTable.objects.create(destroyed=expiry_table,quantity_destroyed=quantity_need,destroyer=(user.first_name+" "+user.last_name))
        drug_track.save()
        serializer=DrugTrackTableSerializer(drug_track)
        return Response(serializer.data)
