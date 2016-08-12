import logging

from django_rq import job

from src.apps.read_model.key_value.prospect import service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('default')
def add_prospect_to_deleted_set_task(prospect_id):
  pass
  # log_message = (
  #   "prospect_id: %s",
  #   prospect_id
  # )
  #
  # with log_wrapper(logger.info, *log_message):
  #   return service.add_prospect_to_deleted_set(prospect_id)


@job('default')
def save_recent_eo_content_task(eo_id, content, external_id, provider_type, provider_action_type, prospect_id):
  log_message = (
    "eo_id: %s, prospect_id: %s", eo_id, prospect_id
  )

  with log_wrapper(logger.info, *log_message):
    return service.save_recent_eo_content(eo_id, content, external_id, provider_type, provider_action_type, prospect_id)
