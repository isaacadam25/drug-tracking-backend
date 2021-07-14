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
        transaction=Transaction.objects.get(id=id)
        transaction_type=TransactionType.objects.get(type_name='purchase')
        batch_received=Batch.objects.get(id=transaction.batch.id)
        transaction.is_accepted=True
        new_trans=Transaction.objects.create(transaction_type=transaction_type,batch=transaction.batch,quantity=transaction.quantity,location_to=transaction.location_to,location_from=transaction.location_from,is_accepted=True)
        new_trans.save()
        link=new_trans.reference_number
        transaction.corresponding_transaction=link
        transaction.save()
        batch_serializer=AcceptBatchSerializer(batch_received)
        serializer=TransactionSerializer(transaction)
        content={'transaction':serializer.data , 'batch_information':batch_serializer.data}
        return Response(content)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class getAllIncomingTransactions(APIView):
    def get(self,request,refno):
        hospital_actual=Institute.objects.get(reference_number=refno)
        # transaction_type=Transaction.objects.
        transactions=Transaction.objects.filter(location_to=hospital_actual).filter(transaction_type__type_name='sales').filter(is_accepted=False)
        serializer=TransactionSerializer(transactions,many=True)
        return Response(serializer.data)

class GetHospitalName(APIView):
    def get(self,request,refno):
        institution=Institute.objects.get(reference_number=refno)
        content={'id':institution.id,'name':institution.name}
        return Response(content)