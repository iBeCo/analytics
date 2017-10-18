from django_elasticsearch_dsl import DocType, Index, fields
from ..models import Device

# Name of the Elasticsearch index
device = Index('device')
# See Elasticsearch Indices API reference for available settings
device.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@device.doc_type
class DeviceDocument(DocType):

    date_modified = fields.DateField()

    class Meta:
        model = Device # The model associated with this DocType

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'device_id',
            'date_created',
            'active',
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True
        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False
        # Paginate the django queryset used to populate the index with the specified size
        # (by default there is no pagination)
        # queryset_pagination = 5000

    def prepare_date_modified(self, instance):
        return instance.date_modified
