from django.shortcuts import render
from rest_framework import generics
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