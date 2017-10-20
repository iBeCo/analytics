from django.conf import settings

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search as SearchClient

class Search(object):
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

        self.objects = SearchClient(using=self.__client, index=index)

    def get_client(self):
        return self.__client

    def execute(self,search_client):
        return search_client.execute()
