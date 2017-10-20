# coding=utf-8
from applications.accounts.elastic import Search
from .exceptions import StoreDoesNotExist
from query import store_search, get_device
from device import INDEX


class Device(Search):

    def __init__(self, using=None):
        self.index = INDEX
        Search.__init__(self, using)

    def __get_store(self, store_id, device_id):

        response = self.get_client().search(
                        index=self.index,
                        body=store_search(store_id, device_id)
        )

        if response['hits']['total'] == 0:
            raise StoreDoesNotExist()
        else:
            return response['hits']['hits']

    def update_store(self, store_id, device_id):
        device = self.get_client().search(
            index=self.index,
            body=get_device(device_id)
        )
        response = self.__get_store(self, store_id, device_id)
        #TODO check store_id matches with response['store_ids']
        #TODO if True:update datetime
        #TODO if False:Append store_id and datetime
