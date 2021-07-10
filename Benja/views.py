from django.shortcuts import render
from rest_framework import status,generics, request
from Benja.user_models import UserProfile, HospitalRoom
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView, Response
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox import views as knox_views
from django.http import HttpResponse
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .pharmacy_models import *
from Benja.sales_models import *
from Benja.hospital_models import *
from Benja.pharmacy_serializers import *
from Benja.pharmacy_models import BenjaBatch as Batch
from DTS.hub_models import Institute
from DTS.transaction_models import Transaction as DTStransaction, TransactionType
from DTS.transaction_serializers import TransactionSerializer as DTSTransactionSerializer
from Benja.hospital_serializers import *
from Benja.user_serializers import UserProfileSerializer,HospitalRoomsSerializer
from Benja.sales_serializers import *
# Create your views here.
#USER APIS
class UsersAPI(generics.ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class RoomAPI(generics.ListCreateAPIView):
    queryset=HospitalRoom.objects.all()
    serializer_class=HospitalRoomsSerializer

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

class UserAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class LoggedUserProfile(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects  
    serializer_class = UserProfileSerializer
    def get_object(self):
        obj = get_object_or_404(self.queryset, actual_user=self.request.user)
        return obj
    # def get_queryset(self):
    #     return self.queryset.filter(actual_user=self.request.user)

#PHARMACY APIS
class MedicineAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Medicine.objects.all()
    serializer_class=MedicineSerializer
class BatchAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Batch.objects.all()
    serializer_class=BatchSerializer
class SupplierAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Supplier.objects.all()
    serializer_class=SupplierSerializer

# class MedicineDetailView(generics.RetrieveCreateDestroyAPIView):
#     permission_classes=(IsAuthenticated,)
#     serializer_class=MedicineSerializer
#     questyset=Medicine.objects
    

# class BatchDetailView(generics.RetrieveCreateDestroyAPIView):
#     permission_classes=(IsAuthenticated,)
#     serializer_class=BatchSerializer
#     queryset=Batch.object

#HOSPITAL APIS.
class PatientAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Patient.objects.all()
    serializer_class=PatientSerializer
class PendingAppointmentAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Appointment.objects.filter(status='pending')
    serializer_class=AppointmentSerializer
class ActiveAppointmentAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Appointment.objects.filter(status='active')
    serializer_class=AppointmentSerializer
class CompleteAppointmentAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Appointment.objects.filter(status='complete')
    serializer_class=AppointmentSerializer
class LabtestAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Labtest.objects.all()
    serializer_class=LabtestSerializer
class LabItemAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=LabTestItem.objects.all()
    serializer_class=LabTestItemSerializer
class DiagnosesAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Diagnosis.objects.all()
    serializer_class=DiagnosisSerializer

class SingleDiagnosesAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Diagnosis.objects.all()
    lookup_url_kwarg='id'
    serializer_class=DiagnosisSerializer

class Prescriptions(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Prescription.objects.all()
    serializer_class=PrescriptionSerializer


class GetAppointmentPrescriptions(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,id):
        #appointment=Appointment.objects.filter(id=id)
        perscription=Prescription.objects.filter(appointment=id)
        serializer=PrescriptionSerializer(perscription,many=True)
        return Response(serializer.data)

class AppointmentAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Appointment.objects.all()
    serializer_class=AppointmentSerializer

class SingleAppointmentAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Appointment.objects.all()
    serializer_class=AppointmentSerializer
    lookup_url_kwarg='id'


# class MedicineDetailView(generics.RetrieveCreateDestroyAPIView):
#     permission_classes=(IsAuthenticated,)
#     def query_set(id):
#         return pass
#     serializer_class=(IsAuthenticated,)

# class BatchDetailView(generics.RetrieveCreateDestroyAPIView):
#     permission_classes=(IsAuthenticated,)
#     def query_set(id):
#         return pass
#     serializer_class=BatchSerializer

#SALES API
class OrderAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
class OrderedItemAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=OrderedItem.objects.all()
    serializer_class=ItemSerializer
class InvoiceAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Invoice.objects.all()
    serializer_class=InvoiceSerializer

class TransactionAPI(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Transaction.objects.all()
    serializer_class=TransactionSerializer

class PatientTypeAPI(generics.ListCreateAPIView):
    permission_classes= (IsAuthenticated,)
    queryset=PatientType.objects.all()
    serializer_class=PatientTypeSerializer

###############################PRESCRIPITON#######################
class AcceptPrescriptionAPI(APIView):
    def patch(self,request,id,format=None):
        anonymous_user=self.request.user
        transaction_type=TransactionType.objects.get(type_name='sales')
        hospital_actual=Institute.objects.get(reference_number='INS60541124')
        prescription=Prescription.objects.get(id=id)
        prescription.is_sold=True
        new_trans=DTStransaction.objects.create(transaction_type=transaction_type,batch=prescription.batch,quantity=prescription.quantity,location_to=hospital_actual,location_from=hospital_actual,is_accepted=True)
        prescription.save()
        new_trans.save()
        serializer=PrescriptionSerializer(prescription)
        return Response(serializer.data)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SinglePrescriptionAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Prescription.objects.all()
    lookup_url_kwarg='id'
    serializer_class=PrescriptionSerializer

class BatchAddAPI(APIView):
    def post(self,request,id):
        serializer=BatchSerializer(data=request.data)
        all_batch_no=Batch.objects.values('batch_number').distinct()
        batch_no_1=serializer.data['batch_number']
        if batch_no_1 in all_batch_no:
            quantity_received=serializer.data['quantity_received']
            existing_batch=Batch.objects.get(batch_number=batch_no_1)
            existing_batch.quantity_received=existing_batch.quantity_received+quantity_received
            existing_batch.save()
            serializer=BatchSerializer(existing_batch)
            Response(serializer.data,status=status.HTTP_201_CREATED)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




