import logging

from django_rq import job

from src.apps.relational.prospect import service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_profile_lookup_by_provider_task(profile_id, external_id, provider_type, prospect_id):
  log_message = (
    "profile_id: %s, external_id: %s, provider_type: %s",
    prospect_id, external_id, provider_type
  )

  with log_wrapper(logger.info, *log_message):
    return service.save_profile_lookup_by_provider(profile_id, external_id, provider_type, prospect_id)


@job('high')
def save_eo_lookup_by_provider_task(eo_id, external_id, provider_type, prospect_id):
  log_message = (
    "eo_id: %s, external_id: %s, provider_type: %s",
    eo_id, external_id, provider_type
  )

  with log_wrapper(logger.info, *log_message):
    return service.save_eo_lookup_by_provider(eo_id, external_id, provider_type, prospect_id)
