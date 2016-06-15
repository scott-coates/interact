import logging

from django_rq import job

from src.apps.key_value.prospect import service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('default')
def save_eo_topic_set_task(eo_id, topic_id):
  log_message = (
    "eo_id: %s, topic_id: %s",
    eo_id, topic_id
  )

  with log_wrapper(logger.info, *log_message):
    return service.save_eo_topic_set(eo_id, topic_id)
