from django.contrib.auth import get_user_model

from applications.accounts.models import Device


def index_devices():
    User = get_user_model()
    user = User.objects.all()[0]
    for i in range(10):
        device = Device()
        device.user = user
        device.device_id = 'store_' + str(i)
        device.save()

