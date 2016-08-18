import logging
from operator import itemgetter

from django_rq import job

from src.apps.engagement_discovery import service
from src.apps.read_model.key_value.prospect.service import get_recent_prospect_discovery_network
from src.apps.read_model.relational.client.service import get_eo_ea_lookup
from src.domain.common import constants
from src.domain.prospect.service import prospect_is_deleted
from src.domain.prospect.tasks import populate_prospect_from_provider_info_chain
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('default')
def discover_engagement_opportunities_task():
  log_message = "Discover opportunity engagements."

  with log_wrapper(logger.debug, log_message):
    return service.discover_engagement_opportunities()


@job('default')
def discover_engagement_opportunities_from_profile_task(external_id, provider_type, prospect_id):
  log_message = ("external_id: %s, provider_type: %s, prospect_id: %s", external_id, provider_type, prospect_id)

  with log_wrapper(logger.debug, *log_message):
    if prospect_is_deleted(prospect_id):
      logger.info('prospect %s is deleted. aborting task', prospect_id)
    else:
      service.discover_engagement_opportunities_from_profile(external_id, provider_type)


@job('default')
def discover_engagement_opportunities_from_batch_assignments_task(batch_id, assigned_eas):
  log_message = ("batch_id: %s", batch_id)

  with log_wrapper(logger.debug, *log_message):
    discovery_network = service.get_discovery_network_from_batch_assignments(assigned_eas)

    for recent_connection in discovery_network:
      external_id_ = recent_connection[constants.EXTERNAL_ID]
      provider_type = recent_connection[constants.PROVIDER_TYPE]
      # populate_prospect_from_provider_info_chain.delay(external_id_, provider_type)
