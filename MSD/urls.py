
from django.urls import path
from .views import *



urlpatterns=[
    path('stock/medicine/<int:id>',MedicineDetailView.as_view(),name="medicine"),
    path('stock/medicine',MedicineAPI.as_view(),name="medicine"),
    path('stock/medicine/remaining',RemainingMedicineMSD.as_view(),name="remaining-medicine"),
    path('order',CreateViewOrdersAPI.as_view(),name="order"),
    path('order-items/<int:pk>/',CreateViewOrderItemAPI.as_view(),name="order-item"),
    path('order/latest',LatestOrderAPI.as_view(),name="latest-order"),
    path('order/<int:id>',SingleOrderAPI.as_view(),name="single-order"),

]
   