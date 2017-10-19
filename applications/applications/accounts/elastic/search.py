# coding=utf-8
from django.conf import settings

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search as ElasticSearch

class Search(object)
    """
    A base class for all the search operations
    """
    def __init__(self,index,using=None):
        """
        :param chart_of_account:
        :return:

        Initialise the Base Journal
        """
        if using is None:
            self.__client = Elasticsearch()
        else:
            self.__client = Elasticsearch()

        self.objects = Search(using=self.__client, index=index)

    def get_client(self):
        return self.__client

class Device(Search):

    def __init__(self,using=None):
        Search.__init__(self, using)

    def has_store(self, store_id)
        s = Search(using=client, index="my-index")
