import logging

from src.apps.graph.client import service as client_graph_service
from src.domain.client.commands import AddEA
from src.domain.common import constants
from src.libs.common_domain import dispatcher
from src.libs.python_utils.id.id_utils import generate_id

logger = logging.getLogger(__name__)


def refresh_assignments(client_id, assignment_group, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  prospect_id = assignment_group[constants.PROSPECT_ID]

  assignment_attrs = {}

  eo_ids = assignment_group.get(constants.EO_IDS)
  if eo_ids: assignment_attrs[constants.EO_IDS] = eo_ids

  ea_id = generate_id()
  add_ea = AddEA(ea_id, assignment_attrs, prospect_id)
  _dispatcher.send_command(client_id, add_ea)


def get_unassigned_grouped_entities_for_client(client_id):
  ret_val = client_graph_service.get_unassigned_grouped_entities_for_client_from_graphdb(client_id)

  return ret_val
