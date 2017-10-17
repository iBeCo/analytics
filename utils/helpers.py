# coding=utf-8

import time
import string
from random import Random, randint


from django.conf import settings

from rest_framework import status


USING_AWS_S3 = getattr(settings, 'USE_AWS_S3', False)



class UtlRandom:
    '''
    Random # generation
    '''
    random = ""

    def __init__(self):
        self.random = Random(x=time.time())

    def random_str(self, n):
        return ''.join(self.random.choice(string.ascii_uppercase +
                                          string.digits) for _ in range(n))

    def random_num(self, b, e):
        return self.random.randint(b, e)

    def random_username(self, length):
        return ''.join(self.random.choice(string.lowercase) for i in range(length))

    def random_email(self, length):
        email_host = 'example.com'
        random_username = self.random_username(length)
        return random_username+'@'+email_host


class ErrorType(object):

    NOT_AUTHORIZED = status.HTTP_401_UNAUTHORIZED
    NOT_FOUND = status.HTTP_404_NOT_FOUND
    SUCCESS = status.HTTP_200_OK
    MISSING_ATTRIBUTES = status.HTTP_206_PARTIAL_CONTENT
    NOT_MODIFIED = status.HTTP_304_NOT_MODIFIED
    BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    CONFLICT = status.HTTP_409_CONFLICT
    NOT_ACCEPTABLE = status.HTTP_406_NOT_ACCEPTABLE
    NOT_ALLOWED = status.HTTP_405_METHOD_NOT_ALLOWED
