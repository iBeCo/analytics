from django.contrib import admin

from applications.accounts.models import User, Device

admin.site.register(User)
admin.site.register(Device)

