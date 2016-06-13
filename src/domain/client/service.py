import logging

from src.apps.graph.client import service as client_graph_service
from src.domain.client.commands import AddEA
from src.domain.common import constants
from src.libs.common_domain import dispatcher
from src.libs.python_utils.id.id_utils import generate_id
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


def refresh_assignments(client_id, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  method_log_message = (
    "Refresh assignments for client_id: %s",
    client_id
  )

  with log_wrapper(logger.debug, *method_log_message):
    counter = 1

    entities_to_add = get_unassigned_grouped_entities_for_client(client_id)

    total_assignments_count = len(entities_to_add)

    logger.debug("Assignments to create for client_id: %s: %i", client_id, total_assignments_count)

    for group in entities_to_add:
      group_log_message = ("Assignment: %i out of %i for client_id: %s", counter, total_assignments_count, client_id)

      with log_wrapper(logger.debug, *group_log_message):

        assignment_attrs = {}

        eo_ids = group.get(constants.EO_IDS)
        if eo_ids: assignment_attrs[constants.EO_IDS] = eo_ids

        ea_id = generate_id()
        try:
          add_ea = AddEA(ea_id, assignment_attrs)
          _dispatcher.send_command(client_id, add_ea)
        except Exception as e:
          logger.warn("Error creating assignment", exc_info=True)

        counter += 1


def get_unassigned_grouped_entities_for_client(client_id):
  ret_val = client_graph_service.get_unassigned_grouped_entities_for_client_from_graphdb(client_id)

  return ret_val
