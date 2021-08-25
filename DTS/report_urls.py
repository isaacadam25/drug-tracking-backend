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
    path('batch/trace/<str:batchno>',BatchTrace.as_view(),name="remain-medicine"),
    path('batch/track/missing',GetBatchLost.as_view(),name="lost-medicines"),
    path('batch/track/lost',GetBatchLostFromMSD.as_view(),name="lost-batches"),
    path('batch/track/most-used',MostUsedBatches.as_view(),name="most-used-batches"),
    path('batch/total/used',AllUsedDrugs.as_view(),name="total-used"),
    path('batch/total/registered',AllReceivedDrugs.as_view(),name="total-registered"),
    path('batch/total/lost',AllLostDrugs.as_view(),name="total-lost"),
    
    path('batch/track/need-destroy/<str:refno>',GetDrugsNeedDestroying.as_view(),name="destroy-batches"),
    path('batch/track/most-destroyed',GetMostExpiredMedicines.as_view(),name="most-destroyed"),
    path('batch/track/expire-trends/<int:year>',ExpireTrends.as_view(),name="expire-trends"),
    path('batch/track/piechard/medicine-used/<int:batchid>',MedicineUsedPieChartAPI.as_view(),name="medicine_used_pie"),
    path('batch/used/expired',GetPercentageOfExpiredUsed.as_view(),name="usage_expired"),
    path('transaction/log',TransactionLog.as_view(),name="transaction-log"),
    path('transaction/distribution/<str:batchno>',BatchDistribution.as_view(),name="distribution"),
    path('batch/track/lost-hospital',GetMissingHospitalDrugs.as_view(),name="lost-hospital-drugs"),
    path('batch/track/drug-track-table',DrugTrackTableAPI.as_view(),name="drug-track"),
    path('batch/track/destroy-api',DestroyAPI.as_view(),name="destroy-api")



]