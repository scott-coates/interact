import logging

from django_rq import job

from src.apps.key_value.client import service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_active_client_task(id):
  log_message = ("client_id: %s", id)

  with log_wrapper(logger.info, *log_message):
    return service.save_active_client(id)
