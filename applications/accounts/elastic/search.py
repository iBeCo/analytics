# coding=utf-8
from applications.accounts.elastic import Search
from elasticsearch_dsl import Q
from exceptions import StoreDoesNotExist
from query import store_search
from device import INDEX

class Device(Search):

    def __init__(self,using=None):
        self.index = INDEX
        Search.__init__(self,using)

    def get_store(self, store_id,id):

        response = self.get_client().search(
                        index=self.index,
                        body=store_search(store_id,id))

        if response['hits']['total'] == 0:
            raise StoreDoesNotExist()
        else:
            return response['hits']['hits']
