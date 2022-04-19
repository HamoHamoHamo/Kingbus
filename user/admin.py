from django.contrib import admin
from user.models import *
# Register your models here.

@admin.register(User)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
    )

# admin.site.register(User)
admin.site.register(DriverAcc)
admin.site.register(CompanyAcc)
admin.site.register(KingbusReview)