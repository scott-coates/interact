import logging

from src.apps.read_model.relational.client.service import save_batch_ea, get_assignment_batch
from src.domain.client.commands import AddEaBatch
from src.domain.client.entities import Client
from src.domain.common import constants
from src.libs.common_domain import dispatcher, aggregate_repository
from src.libs.python_utils.id.id_utils import generate_id

logger = logging.getLogger(__name__)


def save_assignment_batch_from_attrs(client_id, assignment_group, batch_id, counter, _aggregate_repository=None):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  client = _aggregate_repository.get(Client, client_id)

  prospect_id = assignment_group[constants.PROSPECT_ID]

  assignment_attrs = {}

  eo_ids = assignment_group.get(constants.EO_IDS)
  if eo_ids: assignment_attrs[constants.EO_IDS] = eo_ids

  score, score_attrs = client.calculate_engagement_assignment_score(assignment_attrs)
  save_batch_ea(generate_id(), assignment_attrs, score, score_attrs, client_id, batch_id, counter, prospect_id)


def process_assignment_batch(client_id, batch_id, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher
  batch = get_assignment_batch(client_id, batch_id)

  add_ea_batch = AddEaBatch(batch_id, batch)
  _dispatcher.send_command(client_id, add_ea_batch)
