from django.contrib import admin
from .models import *
# Register your models here.

for n in [Medicine,Order,OrderedItem]:
    admin.site.register(n)