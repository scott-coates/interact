import logging

from django_rq import job

from src.domain.prospect import services
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('default')
def save_prospect_from_provider_info_task(profile_external_id, provider_type):
  log_message = ("profile_external_id: %s, provider_type: %s", profile_external_id, provider_type)

  with log_wrapper(logger.info, *log_message):
    return services.save_prospect_from_provider_info_(profile_external_id, provider_type).id


@job('default')
def save_profile_from_provider_info_task(prospect_id, profile_external_id, provider_type):
  log_message = (
    "prospect_id: %s, profile_external_id: %s, provider_type: %s",
    prospect_id, profile_external_id, provider_type
  )

  with log_wrapper(logger.info, *log_message):
    return services.save_profile_from_provider_info(prospect_id, profile_external_id, provider_type).id
