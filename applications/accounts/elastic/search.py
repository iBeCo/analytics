# coding=utf-8
from applications.accounts.elastic import Search
from elasticsearch_dsl import Q
from exceptions import StoreDoesNotExist

class Device(Search):
    search_client = None

    def __init__(self,index,using=None):
        Search.__init__(self, using)

    def get_search_client(self):
        if self.search_client is None:
            return self.objects
        else:
            return self.search_client

    def get_store(self, store_id,id):
        self.search_client = self.get_search_client()
        self.search_client.query = Q('bool', must=[Q('match', stores__store_id=store_id), Q('match', _id=id)])
        self.response = self.execute(self.search_client)
        if not self.response:
            raise StoreDoesNotExist()
        else:
            return self.response[0]
