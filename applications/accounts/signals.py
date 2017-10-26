# coding=utf-8

from django.apps import apps

import hmac
import hashlib
import base64

from rest_framework import authentication
from rest_framework import exceptions
from httpsig import HeaderSigner
import re

# dig = hmac.new(b'1234567890', msg=your_bytes_string, digestmod=hashlib.sha256).digest()
# base64.b64encode(dig).decode()      # py3k-mode
# 'Nace+U3Az4OhN7tISqgs1vdLBHBEijWcBeCqL5xN9xg='


def add_signature_signal(sender, **kwargs):
    instance = kwargs.pop('instance')
    generate_signature(instance.id)


def generate_signature(id):
    User = apps.get_model(app_label='accounts', model_name='User')
    avatar = User.objects.get(id=id)
    while not avatar.signature:
        computed_string = build_signature(avatar.api_key, avatar.secret_key)
        computed_signature = get_signature_from_signature_string(computed_string)
        signature = computed_signature
        user_exists = User.objects.filter(signature=signature)
        if user_exists.count() == 0:
            avatar.signature = signature
            avatar.save()


# Signature creation

SIGNATURE_RE = re.compile('signature="(.+?)"')
SIGNATURE_HEADERS_RE = re.compile('headers="([\(\)\sa-z0-9-]+?)"')

API_KEY_HEADER = 'X-Api-Key'
ALGORITHM = 'hmac-sha256'


def get_signature_from_signature_string(signature):
    """Return the signature from the signature header or None."""
    match = SIGNATURE_RE.search(signature)
    if not match:
        return None
    return match.group(1)


def build_signature(user_api_key, user_secret):
    """Return the signature for the request."""
    signer = HeaderSigner(
        key_id=user_api_key, secret=user_secret,
        headers=['date'], algorithm=ALGORITHM)
    signed = signer.sign({'date': None}, method="POST", path='/ad/stores/45/iamhere/')
    return signed['authorization']
