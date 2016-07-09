import logging

from django_rq import job

from src.apps.key_value.prospect import service
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
