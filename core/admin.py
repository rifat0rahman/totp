from django.contrib import admin

from .models import TOTP, Device,Authenticate
# Register your models here.
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['location_ID','seed','otp']



admin.site.register(Device,DeviceAdmin)
admin.site.register(Authenticate)

admin.site.register(TOTP)