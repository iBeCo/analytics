# coding=utf-8
from applications.accounts.elastic import Search
from .exceptions import StoreDoesNotExist
from query import store_search, get_device
from device import INDEX
from datetime import datetime




class Device(Search):

    def __init__(self, using=None):
        self.index = INDEX
        Search.__init__(self, using)

    def __get_store(self, store_id, device_id):

        response = self.get_client().search(
                        index=self.index,
                        body=store_search(store_id, device_id))

        if response['hits']['total'] == 0:
            raise StoreDoesNotExist()
        else:
            return response['hits']['hits']

    def update_store(self, store_id, device_id):
        import ipdb; ipdb.set_trace();
        device = self.get_client().search(
            index=self.index,
            body=get_device(device_id))
        document_id = int(device['hits']['hits'][0]['_id'])
        print device['hits']['total']
        response = self._Device__get_store(store_id, device_id)
        if response:
            #TODO if True:update datetime
            es = self.get_client()
            es.update(index=self.index, doc_type='device_document', id=document_id, body={"doc": {"stores.date": datetime.now()}})
        else:
            #TODO if False:Append store_id and datetime
            pass

