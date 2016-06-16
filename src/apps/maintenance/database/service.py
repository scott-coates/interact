from django.contrib.contenttypes.models import ContentType

from src.libs.graphdb_utils.services import graphdb_provider
from src.libs.graphdb_utils.services.graphdb_service import purge_data
from src.libs.key_value_utils.key_value_provider import get_key_value_client


def clear_read_model():
  gdb = graphdb_provider.get_graph_client()
  purge_data(gdb)

  kdb = get_key_value_client()
  read_model_keys = kdb.keys('read_model:*')
  for r in read_model_keys:
    kdb.delete(r)

  read_model_types = ContentType.objects.filter(app_label='relational')
  for read_model_type in read_model_types:
    read_model_type.model_class().objects.all().delete()
