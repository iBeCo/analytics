# coding=utf-8
from applications.account.elastic import Search

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
        self.search_client = self.filter(self.get_search_client(),store_id="stores.store_id", id="_id")
        return self.execute(self.search_client)
