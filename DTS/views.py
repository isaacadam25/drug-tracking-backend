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
# Create your views here.


#############################USER_VIEWS#############################
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=UserSerializer
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
class LoginAPI(KnoxLoginView):
    permission_classes = [AllowAny,]
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
class UserProfileView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = RestrictedUserSerializer

class LoggedUserProfile(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects  
    serializer_class = UserProfileSerializer
    def get_object(self):
        obj = get_object_or_404(self.queryset, actual_user=self.request.user)
        return obj


#############################STOCK_VIEWS############################


class AcceptAPI(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Transaction.objects.all()
    serializer_class=TransactionSerializer
    lookup_url_kwarg = 'id'

class SingleManufacturerAPI(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Manufacturer.objects.all()
    serializer_class=ManufacturerSerializer
    lookup_url_kwarg = 'id'

class ActiveManufacturerAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Manufacturer.objects.filter(is_active=True)
    serializer_class=ManufacturerSerializer

class ManufacturerAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Manufacturer.objects.all()
    serializer_class=ManufacturerSerializer

class SuspendedManufacturerAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Manufacturer.objects.filter(is_active=False)
    serializer_class=ManufacturerSerializer






class GetExpiredBatches(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Batch.objects.filter(expiry_date__lte=datetime.date.today())
    serializer_class=BatchSerializer

class GetSingleExpiredBatch(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Batch.objects.filter(expiry_date__lte=datetime.date.today())
    serializer_class=BatchSerializer
    lookup_url_kwarg='id'




class MedicineTypeAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=MedicineType.objects.all()
    serializer_class = MedicineTypeSerializer

class BatchAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Batch.objects.all()
    serializer_class=BatchSerializer

class BatchAddAPI(APIView):
    def post(self,request):
        all_manufacturer=list(MedicineDetails.objects.values_list('manufacturer__name',flat=True).distinct())
        all_medicine_name=list(MedicineDetails.objects.values_list('name',flat=True).distinct())
        # batch_no_1=serializer.data['batch_number']
        man=request.data['manufacturer']
        medicine_name=request.data['name']
        batch_number=request.data['batch_number']
        concentration=request.data['concentration']
        quantity_received=request.data['quantity_received']
        unit_of_measure=request.data['unit_of_measure']
        production_date=request.data['production_date']
        expiry_date=request.data['expiry_date']
        description=request.data['description']
        manufacturer=Manufacturer.objects.get(id=man)

        medicine_type=MedicineType.objects.get(id=request.data['medicine_type'])
        if medicine_name in all_medicine_name and manufacturer in all_manufacturer:
            existing_medicine_detail=MedicineDetails.objects.filter(name=medicine_name).filter(manufacturer=manufacturer)
            new_batch=Batch.objects.create(description=description,medicine_detail=existing_medicine_detail[0],batch_number=batch_number,concentration=concentration,quantity_received=quantity_received,unit_of_measure=unit_of_measure,production_date=production_date,expiry_date=expiry_date,medicine_type=medicine_type)

        else:
            new_medicine_detail=MedicineDetails.objects.create(name=medicine_name,manufacturer=manufacturer) 
            new_batch=Batch.objects.create(description=description,medicine_detail=new_medicine_detail,batch_number=batch_number,concentration=concentration,quantity_received=quantity_received,unit_of_measure=unit_of_measure,production_date=production_date,expiry_date=expiry_date,medicine_type=medicine_type)

            
        new_batch.save()
        approve=Approval()
        approve.id=new_batch
        approve.save()
        serializer=BatchSerializer(new_batch)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
   


        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data,
        #                     status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BatchUpdateAPI(APIView):
    def put(id,request):
        all_manufacturer=list(MedicineDetails.objects.values_list('manufacturer',flat=True).distinct())
        all_medicine_name=list(MedicineDetails.objects.values_list('name',flat=True).distinct())
        # batch_no_1=serializer.data['batch_number']
        manufacturer=request.data['manufacturer']
        medicine_name=request.data['name']
        batch_number=request.data['batch_number']
        concentration=request.data['concentration']
        quantity_received=request.data['quantity_received']
        unit_of_measure=request.data['unit_of_measure']
        production_date=request.data['production_date']
        expiry_date=request.data['expiry_date']
        medicine_type=MedicineType.objects.get(id=request.data['medicine_type'])
        if medicine_name in all_medicine_name and manufacturer in all_manufacturer:
            medicine_detail=MedicineDetails.objects.filter(name=medicine_name).filter(manufacturer=manufacturer)
        else:
            medicine_detail=MedicineDetails.objects.create(name=medicine_name,manufacturer=manufacturer) 
            
        old_batch=Batch.objects.get(id=id)
        old_batch.medicine_detail=medicine_detail
        old_batch.quantity_received=quantity_received
        old_batch.batch_number=batch_number
        old_batch.concentration=concentration
        old_batch.unit_of_measure=unit_of_measure
        old_batch.production_date=production_date
        old_batch.expiry_date=expiry_date
        old_batch.medicine_type=medicine_type
        old_batch.save()
        serializer=BatchSerializer(old_batch)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)


class BatchUnapprovedAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Approval.objects.filter(status=False).filter(is_declined=False)
    serializer_class=BatchApprovalSerializer

class BatchDeclinedAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Approval.objects.filter(is_declined=True)
    serializer_class=BatchApprovalSerializer

class SingleBatchDeclinedAPI(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Approval.objects.filter(is_declined=True)
    serializer_class=BatchApprovalSerializer
    lookup_url_kwarg = 'id'


class BatchApprovedAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Approval.objects.filter(status=True).order_by("-date_approved")
    serializer_class=BatchApprovalSerializer

class ApprovedUnExpiredDrugs(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Approval.objects.filter(status=True).filter(id__expiry_date__gt=datetime.date.today())
    serializer_class=BatchApprovalSerializer

class SingleBatchApprovedAPI(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Approval.objects.filter(status=True)
    serializer_class=BatchApprovalSerializer
    lookup_url_kwarg = 'id'

class UpdateSingleBatchAPI(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Approval.objects.all()
    serializer_class=BatchApprovalSerializer
    lookup_url_kwarg = 'id'

class SingleUnapprovedBatchAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Approval.objects.all()
    serializer_class=BatchApprovalSerializer
    lookup_url_kwarg = 'id'

class SingleEditDeleteBatchAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Batch.objects.all()
    serializer_class=BatchSerializer
    lookup_url_kwarg = 'id'
# class BatchapprovalStatusUpdate(generics.RetrieveUpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset=Batch.objects.filter(approval.status==False)
#     serializer_class=BatchApprovalSerializer
#     fields=['approval_status']


class MedicineInfoView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=MedicineInformationSerializer
    queryset=MedicineDetails.objects.all()

class LatestMedicinelView(generics.RetrieveAPIView):
    serializer_class=MedicineInformationSerializer
    # lookup_url_kwarg='date_added'
    queryset=MedicineDetails.objects.all()
    def get_object(self, *args, **kwargs):
        return self.queryset.latest('date_added')
#############################HUB_VIEWS############################
class InstituteAPI(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    queryset=Institute.objects.all()
    serializer_class=InstituteSerializer

class DistributionAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Institute.objects.filter(~Q(institute_type__name="tmda")).filter(~Q(institute_type__name="moh")).filter(~Q(institute_type__name="msd")).filter(~Q(institute_type__name="government"))
    serializer_class=InstituteSerializer

class SingleDistributionAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Institute.objects.filter(~Q(institute_type__name="tmda")).filter(~Q(institute_type__name="moh")).filter(~Q(institute_type__name="msd")).filter(~Q(institute_type__name="government"))
    serializer_class=InstituteSerializer
    lookup_url_kwarg = 'id'

class LocationAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Local.objects.all()
    serializer_class=LocationSerializer

#############################TRANSACTION_VIEWS############################
class TransactionAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Transaction.objects.all()
    serializer_class=TransactionSerializer

class PurchaseTransactionAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Transaction.objects.filter(transaction_type__type_name='purchase')
    serializer_class=TransactionSerializer

class CreateTransactionAPI(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Transaction.objects.all()
    serializer_class=CreateTransactionSerializer

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=TransactionSerializer
    lookup_url_kwarg = 'id'
    queryset=Transaction.objects.all()

class TransactionTypeAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=TransactionType.objects.all()
    serializer_class=TransactionTypeSerializer

class ViewUnacceptedTransactionListAPI(generics.ListAPIView):
    def get(self,request,ref):
        unaccepted=Transaction.objects.filter(location_to__reference_number=ref).filter(is_accepted=False).filter(transaction_type__type_name='sales')
        serializer=TransactionSerializer(unaccepted,many=True)
        return Response(serializer.data)

class ViewUnacceptedTransactionListMSDAPI(generics.ListAPIView):
    def get(self,request):
        unaccepted=Transaction.objects.filter(location_from__name='msd').filter(is_accepted=False).filter(transaction_type__type_name='sales')
        serializer=TransactionSerializer(unaccepted,many=True)
        return Response(serializer.data)

class ViewAcceptedTransactionListMSDAPI(generics.ListAPIView):
    def get(self,request):
        accepted=Transaction.objects.filter(location_from__name='msd').filter(is_accepted=True).filter(transaction_type__type_name='sales')
        serializer=TransactionSerializer(accepted,many=True)
        return Response(serializer.data)

class ViewAllTransactionListMSDAPI(generics.ListAPIView):
    def get(self,request):
        all=Transaction.objects.filter(location_from__name='msd').filter(transaction_type__type_name='sales')
        serializer=TransactionSerializer(all,many=True)
        return Response(serializer.data)

class AcceptTransactionAPI(APIView):
    def patch(self,request,id,format=None):
        quant=request.data['quantity_received']
        transaction=Transaction.objects.get(id=id)
        transaction_type=TransactionType.objects.get(type_name='purchase')
        transacted_user=self.request.user
        profile=UserProfile.objects.get(actual_user=transacted_user)
        batch_received=Batch.objects.get(id=transaction.batch.id)
        transaction.is_accepted=True
        new_trans=Transaction.objects.create(corresponding_transaction=transaction.reference_number,transaction_type=transaction_type,batch=transaction.batch,quantity=quant,location_to=transaction.location_to,location_from=transaction.location_from,is_accepted=True,initiator=profile)
        new_trans.save()
        link=new_trans.reference_number
        transaction.corresponding_transaction=link
        transaction.save()
        batch_serializer=AcceptBatchSerializer(batch_received)
        serializer=TransactionSerializer(new_trans)
        content={'transaction':serializer.data , 'batch_information':batch_serializer.data}
        return Response(content)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class getAllIncomingTransactions(APIView):
    def get(self,request,refno):
        hospital_actual=Institute.objects.get(reference_number=refno)
        # transaction_type=Transaction.objects.
        transactions=Transaction.objects.filter(location_to=hospital_actual).filter(location_from__name="msd").filter(transaction_type__type_name='sales').filter(is_accepted=False)
        serializer=TransactionSerializer(transactions,many=True)
        return Response(serializer.data)

class getAllHospitalTransactions(APIView):
    permission_classes=(AllowAny,)
    def get(self,request,refno):
        hospital_actual=Institute.objects.get(reference_number=refno)
        # transaction_type=Transaction.objects.
        transactions=Transaction.objects.filter(location_to=hospital_actual).filter(location_from__name='msd').filter(transaction_type__type_name='purchase')
        serializer=TransactionSerializer(transactions,many=True)
        return Response(serializer.data)

class GetHospitalName(APIView):
    def get(self,request,refno):
        institution=Institute.objects.get(reference_number=refno)
        content={'id':institution.id,'name':institution.name}
        return Response(content)

