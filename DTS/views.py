from django.shortcuts import render
from rest_framework import status,generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.db.models import Q

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
class MedicineAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Medicine.objects.all()
    serializer_class=MedicineSerializer


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

class BatchApprovedAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Approval.objects.filter(status=True)
    serializer_class=BatchApprovalSerializer

class UpdateSingleBatchAPI(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Approval.objects.all()
    serializer_class=BatchApprovalSerializer
    lookup_url_kwarg = 'id'

# class BatchapprovalStatusUpdate(generics.RetrieveUpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset=Batch.objects.filter(approval.status==False)
#     serializer_class=BatchApprovalSerializer
#     fields=['approval_status']


class MedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=MedicineSerializer
    lookup_url_kwarg = 'id'
    queryset=Medicine.objects.all()

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
    queryset=Institute.objects.filter(~Q(name="TMDA")).filter(~Q(name="MSD"))
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