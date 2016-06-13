import logging

from src.apps.graph.client import service as client_graph_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


def refresh_assignments(client_id):
  method_log_message = (
    "Refresh assignments for client: %s",
    client_id
  )

  with log_wrapper(logger.debug, *method_log_message):
    counter = 1
    entities_to_add = get_unassigned_grouped_entities_for_client(client_id)


def get_unassigned_grouped_entities_for_client(client_id):
  ret_val = client_graph_service.retrieve_unassigned_grouped_entities_for_client_from_graphdb(client_id)

  return ret_val
