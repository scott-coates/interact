from src.libs.graphdb_utils.services import graphdb_provider
from src.libs.graphdb_utils.services.graphdb_service import purge_data
from src.libs.key_value_utils.key_value_provider import get_key_value_client


def clear_read_model():
  gdb = graphdb_provider.get_graph_client()
  purge_data(gdb)

  kdb = get_key_value_client()
  kdb.flushall()
