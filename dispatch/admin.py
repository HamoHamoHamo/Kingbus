from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Dispatch)
admin.site.register(Dispatch_estimate)
admin.site.register(Dispatch_order)
admin.site.register(Regularly_order)

