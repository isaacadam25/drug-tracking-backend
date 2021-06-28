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


class GetExpiredBatches(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Batch.objects.filter(expiry_date__lte=datetime.date.today())
    serializer_class=BatchSerializer

class GetSingleExpiredBatch(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Batch.objects.filter(expiry_date__lte=datetime.date.today())
    serializer_class=BatchSerializer
    lookup_url_kwarg='id'

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


class MedicineTypeAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=MedicineType.objects.all()
    serializer_class = MedicineTypeSerializer

class BatchAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Batch.objects.all()
    serializer_class=BatchSerializer


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
    queryset=Approval.objects.filter(status=True)
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

class SingleUnapprovedBatchAPI(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Approval.objects.filter(status=False).filter(is_declined=False)
    serializer_class=BatchApprovalSerializer
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
    permission_classes = (IsAuthenticated,)
    queryset=Institute.objects.all()
    serializer_class=InstituteSerializer

class DistributionAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Institute.objects.filter(~Q(institute_type__name="tmda")).filter(~Q(institute_type__name="msd")).filter(~Q(institute_type__name="government"))
    serializer_class=InstituteSerializer

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

class AcceptTransactionAPI(APIView):
    def patch(self,request,id,format=None):
        transaction=Transaction.objects.get(id=id)
        transaction_type=TransactionType.objects.get(type_name='purchase')
        transaction.is_accepted=True
        new_trans=Transaction.objects.create(transaction_type=transaction_type,batch=transaction.batch,quantity=transaction.quantity,location_to=transaction.location_to,location_from=transaction.location_from,is_accepted=True)
        transaction.save()
        new_trans.save()
        serializer=TransactionSerializer(transaction)
        return Response(serializer.data)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)