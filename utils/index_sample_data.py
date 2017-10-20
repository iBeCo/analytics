from django.contrib.auth import get_user_model

from datetime import datetime

from applications.accounts.models import Device
from applications.accounts.elastic.device import DeviceDocument



# create and save devices using django models
def index_devices():
    User = get_user_model()
    user = User.objects.all()[0]
    for i in range(10):
        device = Device()
        device.user = user
        device.device_id = 'store_' + str(i)
        device.save()



# create and save and device using DocType
def add_devices_to_index():
    # create and save a device
    device = DeviceDocument(meta={'id': 40}, decvice_id='kingsmen')
    now = datetime.now()

    device.user = {
        'mobile': '9447606310',
        'email': 'febin@becoapp.in',
    }

    device.stores = {
        'store_id': 'mgroad_2334',
        'date': now,
    }

    device.save()

