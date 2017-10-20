from django.conf import settings

from elasticsearch import Elasticsearch

class Search(object):
    """
    A base class for all the search operations
    """
    def __init__(self,using=None):
        """
        :param chart_of_account:
        :return:

        Initialise the Base Journal
        """
        if using is None:
            self.__client = Elasticsearch()
        else:
            self.__client = Elasticsearch()

    def get_client(self):
        return self.__client
