import logging
from operator import itemgetter

from src.apps.engagement_discovery.providers.twitter.tasks import discover_engagement_opportunities_task, \
  discover_engagement_opportunities_from_user_task
from src.apps.read_model.key_value.prospect.service import get_recent_prospect_discovery_network
from src.domain.common import constants

logger = logging.getLogger(__name__)


def discover_engagement_opportunities():
  discover_engagement_opportunities_task.delay()


def discover_engagement_opportunities_from_profile(external_id, provider_type):
  if provider_type == constants.Provider.TWITTER:
    discover_engagement_opportunities_from_user_task.delay(external_id)


def get_discovery_network_from_batch_assignments(assigned_eas):
  ret_val = []
  # get top 10% scoring assigned_eas
  total = len(assigned_eas)
  top_eas = round(total / 10)

  eas_to_take = sorted(assigned_eas, key=itemgetter('score'), reverse=True)[:top_eas]
  # don't get scores that negatively scored (spam, bad words, etc.) even if in 90 percentile.
  eas_to_take = [e for e in eas_to_take if e[constants.SCORE] >= 0]

  for ea in eas_to_take:
    # each ea gets own task
    prospect = ea[constants.PROSPECT]
    prospect_id = prospect[constants.ID]
    recent_discovery_network = get_recent_prospect_discovery_network(prospect_id)
    ret_val.extend(recent_discovery_network)

  return ret_val
