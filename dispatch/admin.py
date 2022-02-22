from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Dispatch)
admin.site.register(DispatchEstimate)
admin.site.register(DispatchOrder)
admin.site.register(RegularlyOrder)

