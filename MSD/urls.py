
from django.urls import path
from .views import *



urlpatterns=[
    path('stock/medicine/<int:id>',MedicineDetailView.as_view(),name="medicine"),
    path('stock/medicine',MedicineAPI.as_view(),name="medicine"),

]
   