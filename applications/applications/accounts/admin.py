from django.contrib import admin

from applications.accounts.models import User, Device, ArrivalDetection

admin.site.register(User)
admin.site.register(Device)
admin.site.register(ArrivalDetection)

