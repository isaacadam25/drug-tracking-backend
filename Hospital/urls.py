from django.urls import path
from .views import *


urlpatterns = [
    path('userprofile/',LoggedUserProfile.as_view(), name='singleuserprofile'),
    path('userslist/',UserProfileView.as_view(),name="userprofile"),
    path('pharmacy/medicine',MedicineAPI.as_view(),name="medicine"),
    path('pharmacy/batches',BatchAPI.as_view(),name="batch"),
    path('pharmacy/suppliers',SupplierAPI.as_view(),name="suppliers"),
    path('sales/orders',OrderAPI.as_view(),name="orders"),
    path('sales/ordereditems',OrderedItemAPI.as_view(),name="items"),
    path('sales/invoices',InvoiceAPI.as_view(),name="ordeinvoicers"),
    #path('Appointment',AppointmentAPI.as_view(),name="appointment"),
    path('sales/transactions',TransactionAPI.as_view(),name="transactions"),
    path('hospital/patients/',PatientAPI.as_view(),name="patients"),
    path('hospital/appointments/pending/',AppointmentAPI.as_view(),name="pending-appointment"),
    path('hospital/appointments/complete',CompleteAppointmentAPI.as_view(),name="complete-appointment"),
    path('hospital/appointments/active',ActiveAppointmentAPI.as_view(),name="active-appointment"),
    path('hospital/labtests',LabtestAPI.as_view(),name="labtests"),
    path('hospital/labitems',LabItemAPI.as_view(),name="labitems"),

]
