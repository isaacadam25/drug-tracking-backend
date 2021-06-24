from django.urls import path,include
from django.contrib import admin
from Hospital.views import LoginAPI
from DTS.views import LoginAPI as Log


urlpatterns = [
    path('admin/', admin.site.urls),
    path('apis/v1/hospital/',include('Hospital.urls')),
    path('apis/v1/dts/',include('DTS.urls')),
    path('apis/v1/dts/login/',Log.as_view(),name="login"),
    path('apis/v1/hospital/login/',LoginAPI.as_view(),name="login")
]
