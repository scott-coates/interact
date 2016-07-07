import logging

from src.apps.graph.client import service as client_graph_service
from src.apps.key_value.client import service as kv_client_service
from src.apps.relational.client.models import EaToDeliver
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


def get_active_client_ids():
  active_clients_ids = kv_client_service.get_active_client_ids()

  return active_clients_ids


def get_client_ids_ready_for_delivery():
  ret_val = EaToDeliver.objects.values_list('client_id', flat=True).distinct()

  return ret_val


def get_delivery_data_by_client_id(client_id):
  ret_val = EaToDeliver.objects.filter(client_id=client_id).values('id', 'score')

  return ret_val
