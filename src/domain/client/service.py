import logging

from src.apps.relational.client.service import save_batch_ea, get_assignment_batch
from src.domain.client.calculation import calculator
from src.domain.client.commands import AddEaBatch
from src.domain.common import constants
from src.libs.common_domain import dispatcher
from src.libs.python_utils.id.id_utils import generate_id

logger = logging.getLogger(__name__)


def save_assignment_batch_from_attrs(client_id, assignment_group, batch_id, counter, _calculator=None):
  if not _calculator: _calculator = calculator
  prospect_id = assignment_group[constants.PROSPECT_ID]

  assignment_attrs = {}

  eo_ids = assignment_group.get(constants.EO_IDS)
  if eo_ids: assignment_attrs[constants.EO_IDS] = eo_ids

  score, score_attrs = _calculator.calculate_engagement_assignment_score(client_id, assignment_attrs)
  save_batch_ea(generate_id(), assignment_attrs, score, score_attrs, client_id, batch_id, counter, prospect_id)


def process_assignment_batch(client_id, batch_id, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher
  batch = get_assignment_batch(client_id, batch_id)

  add_ea_batch = AddEaBatch(batch_id, batch)
  _dispatcher.send_command(client_id, add_ea_batch)
