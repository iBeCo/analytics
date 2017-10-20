from datetime import datetime

from django_elasticsearch_dsl import DocType, Index, fields
from ..models import Device, User
from elasticsearch import TransportError

# Name of the Elasticsearch index
INDEX = 'device'
device = Index(INDEX)
# See Elasticsearch Indices API reference for available settings
device.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@device.doc_type
class DeviceDocument(DocType):

    date_modified = fields.DateField()

    user = fields.ObjectField(properties={
        'mobile': fields.StringField(),
        'email': fields.StringField(),
    })

    stores = fields.NestedField(properties={
        'store_id': fields.StringField(),
        'date': fields.DateField(),
    })

    '''offers = fields.NestedField(properties={
        'reward': fields.StringField(),
        'date_redeemed': fields.DateField(),
        'expiry_date': fields.DateField(),
        'date_claimed': fields.DateField(),
    })'''

    class Meta:
        model = Device # The model associated with this DocType

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'device_id',
            'date_created',
            'active',
        ]

        related_models = [User]
        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True
        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False
        # Paginate the django queryset used to populate the index with the specified size
        # (by default there is no pagination)
        # queryset_pagination = 5000

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instances from the related model."""
        return related_instance.device_set.all()

    def update_stores(self,store_id):
        # https://github.com/istresearch/kibana-object-format
        self.stores.append({'store_id': store_id,'date': datetime.now()})
        self.save()

    def prepare_stores(self, instance):
        #print instance.stores
        try:
            device = self.get(id=instance.pk)
            return device.stores if device.stores else []
        except TransportError:
            return []

    def prepare_offers(self, instance):
        return []

    def prepare_date_modified(self, instance):
        return instance.date_modified
