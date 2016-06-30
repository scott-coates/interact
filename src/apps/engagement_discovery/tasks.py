import logging

from django_rq import job

from src.apps.engagement_discovery import service
from src.apps.key_value.prospect.service import prospect_is_deleted
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
