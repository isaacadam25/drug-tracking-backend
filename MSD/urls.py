
from django.urls import path
from .views import *



urlpatterns=[
    path('stock/medicine/<int:id>',MedicineDetailView.as_view(),name="medicine"),
    path('stock/medicine',MedicineAPI.as_view(),name="medicine"),
    path('stock/medicine/remaining',RemainingMedicineMSD.as_view(),name="remaining-medicine"),
    path('stock/medicine/available',GetAvailableMSDBAtches.as_view(),name="available-medicine"),
    path('stock/medicine/distributed',GetDistributedMedicines.as_view(),name="distributed-medicine"),
    path('stock/medicine/distributed/quantity',GetDistributedMedicinesQuantity.as_view(),name="distributed-medicine"),
    path('stock/medicine/available/quantity',GetAvailableQuantityMSDBAtches.as_view(),name="available-medicine-quantity"),
    path('stock/medicine/expired',GetExpiredMSDBatches.as_view(),name="remaining-medicine"),
    path('stock/transaction/accepted',GetAllAcceptedBatchesAPI.as_view(),name="accepted-orders"),
    path('stock/transaction/pending',GetExpiredMSDBatches.as_view(),name="pending-orders"),
    path('order',CreateViewOrdersAPI.as_view(),name="order"),
    path('order/create',CreateOrderAPI.as_view(),name="create-order"),
    path('order/send/<int:id>',SendOrderAPI.as_view(),name="send_order"),

    path('order-items',OrderItemAPI.as_view(),name="order-items"),
    path('order-items/<int:pk>/',CreateViewOrderItemAPI.as_view(),name="order-item"),
    path('order-item/<int:id>/',SingleOrderItemAPI.as_view(),name="SINGLE-order-item"),
    path('order/latest',LatestOrderAPI.as_view(),name="latest-order"),
    path('order/<int:id>',SingleOrderAPI.as_view(),name="single-order"),
    path('report/received/<int:year>',GetMedicineReceivedTrends.as_view(),name="received"),
    path('report/used/<int:year>',GetMedicineUsedTrends.as_view(),name="used"),

]
   