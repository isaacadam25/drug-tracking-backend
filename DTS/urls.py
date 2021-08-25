from django.urls import path
from .views import *
from .report_views import *


urlpatterns = [
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('userprofile/',LoggedUserProfile.as_view(), name='singleuserprofile'),
    path('userslist/',UserProfileView.as_view(),name="userprofile"),
    path('stock/medicine-info',MedicineInfoView.as_view(),name="medicine-info"),
    path('stock/medicine-type',MedicineTypeAPI.as_view(),name="medicine-type"),
    path('stock/medicine-latest',LatestMedicinelView.as_view(),name="medicine-latest"),
    path('stock/batches/approval-status/<int:id>',UpdateSingleBatchAPI.as_view(),name="update-batch"),
    path('stock/batches/unapproved/<int:id>',SingleUnapprovedBatchAPI.as_view(),name="single-unapproved-batch"),
    path('stock/batches/<int:id>',SingleEditDeleteBatchAPI.as_view(),name="single-batch"),
    path('stock/batches/approved',BatchApprovedAPI.as_view(),name="approved-batch"),
    path('stock/batches/available',ApprovedUnExpiredDrugs.as_view(),name="available-batch"),
    path('stock/batches/manufacturer',ManufacturerAPI.as_view(),name="get-create-company"),
    path('stock/batches/manufacturer/suspended',SuspendedManufacturerAPI.as_view(),name="get-suspended-company"),
    path('stock/batches/manufacturer/active',ActiveManufacturerAPI.as_view(),name="get-active-company"),
    path('stock/batches/manufacturer/<int:id>',SingleManufacturerAPI.as_view(),name="get-put-company"),

    path('stock/batches/approved/<int:id>',SingleBatchApprovedAPI.as_view(),name="single-approved-batch"),
    path('stock/batches/declined',BatchDeclinedAPI.as_view(),name="declined-batch"),
    path('stock/batches/declined/<int:id>',SingleBatchDeclinedAPI.as_view(),name="single-declined-batch"),
    path('stock/batches/unapproved',BatchUnapprovedAPI.as_view(),name="unapproved-batch"),
    path('stock/batches',BatchAPI.as_view(),name="batch"),
    path('stock/batches/add',BatchAddAPI.as_view(),name="batch-add"),
    path('stock/batches/update/<int:id>',BatchUpdateAPI.as_view(),name="batch-update"),
    path('stock/expired-batches',GetExpiredBatches.as_view(),name="expired-batch"),
    path('stock/expired-batch/<int:id>',GetSingleExpiredBatch.as_view(),name="single-expired"),
    path('transactions/',TransactionAPI.as_view(),name="transactions"),
    path('transactions/purchase',PurchaseTransactionAPI.as_view(),name="transactions"),
    path('transactions/unaccepted/<str:ref>',ViewUnacceptedTransactionListAPI.as_view(),name="unaccepted-transactions"),
    path('transactions/pending',ViewUnacceptedTransactionListMSDAPI.as_view(),name="pending-transactions"),
    path('transactions/accepted',ViewAcceptedTransactionListMSDAPI.as_view(),name="accepted-transactions"),
    path('transactions/all',ViewAllTransactionListMSDAPI.as_view(),name="all-transactions"),
    path('transactions/accept/<int:id>',AcceptTransactionAPI.as_view(),name="unaccepted-transactions"),
    path('transactions/create/',CreateTransactionAPI.as_view(),name="create-transaction"),
    path('transactions/type',TransactionTypeAPI.as_view(),name="transaction-types"),
    path('transactions/details/<int:id>',TransactionDetailView.as_view(),name="transaction_details"),
    
    path('hub/institute/',InstituteAPI.as_view(),name="institute"),
    path('hub/institute/name/<str:refno>',GetHospitalName.as_view(),name="institute-name"),
    path('hub/destinations/',DistributionAPI.as_view(),name="institutes"),
    path('hub/destinations/<int:id>',SingleDistributionAPI.as_view(),name="single-institutes"),
    path('hub/location',LocationAPI.as_view(),name="location"),
    path('hospital/pharmacy/incoming/<str:refno>',getAllIncomingTransactions.as_view(),name="incoming-order"),
    path('hospital/pharmacy/accepted/order/<str:refno>',getAllHospitalTransactions.as_view(),name="all-order"),

]