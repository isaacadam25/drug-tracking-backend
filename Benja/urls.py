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
    path('hospital/labtests',LabtestAPI.as_view(),name="labtests"),
    path('hospital/patients/',PatientAPI.as_view(),name="patients"),
    path('hospital/diagnoses',DiagnosesAPI.as_view(),name="patient-diagnoses"),
    path('hospital/diagnoses/<int:id>',SingleDiagnosesAPI.as_view(),name="single-diagnoses"),

    path('hospital/patient-type',PatientTypeAPI.as_view(),name="patient-type"),
    path('hospital/appointments/',AppointmentAPI.as_view(),name="appointments"),
    path('hospital/appointments/pending',PendingAppointmentAPI.as_view(),name="pending-appointment"),
    path('hospital/appointments/complete',CompleteAppointmentAPI.as_view(),name="complete-appointment"),
    path('hospital/appointments/active',ActiveAppointmentAPI.as_view(),name="active-appointment"),
    path('hospital/appointment/<int:id>',SingleAppointmentAPI.as_view(),name="single-appointment"),
    path('hospital/prescriptions',Prescriptions.as_view(),name="prescriptions"),
    path('hospital/prescriptions/<int:id>',SinglePrescriptionAPI.as_view(),name="single-prescriptions"),
    
    path('hospital/prescriptions/accept/<int:id>',AcceptPrescriptionAPI.as_view(),name="accept-prescriptions"),
    path('hospital/appointment/<int:id>/prescriptions',GetAppointmentPrescriptions.as_view(),name="appointment-prescriptions"),
]
