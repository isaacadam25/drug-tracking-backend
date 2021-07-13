from django.urls import path
from .views import *
from .report_views import *



urlpatterns=[
    path('manufacturers/approved',TopApprovedManufacturersAPI.as_view(),name="top-manufacturer"),
    path('manufacturers/declined',TopDeclinedManufacturersAPI.as_view(),name="top-manufacturer"),
    path('drugs/top-approved',TopApprovedMedicine.as_view(),name="top-medicine"),
    path('drugs/remaining',GetRemainingMedicineHospital.as_view(),name="remain-medicine"),
    path('drugs/remain/<str:refno>',GetRemainingMedicineSingleHospital.as_view(),name="remain-med-hospital"),
    path('drugs/remain/quantity/<str:refno>',GetRemainingMedicineSingleHospitalQuantity.as_view(),name="remain-med-hospital"),
    path('drugs/received/quantity/<str:refno>',GetReceivedMedicineQuantity.as_view(),name="received-med-hospital"),
    path('batch/trace/<int:id>',BatchTrace.as_view(),name="remain-medicine"),
    path('batch/track/missing',GetBatchLost.as_view(),name="lost-medicines"),
]