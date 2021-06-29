from django.urls import path,include
from django.contrib import admin
from Hospital.views import LoginAPI
from DTS.views import LoginAPI as Log

admin.site.site_header = 'Drug Tracking System Admin'
admin.site.site_title = 'Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apis/v1/hospital/',include('Hospital.urls')),
    path('apis/v1/msd/',include('MSD.urls')),
    path('apis/v1/dts/',include('DTS.urls')),
    path('apis/v1/dts/login/',Log.as_view(),name="login"),
    path('apis/v1/hospital/login/',LoginAPI.as_view(),name="login")
]
