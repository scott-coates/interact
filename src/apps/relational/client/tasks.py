import logging

from django_rq import job

from src.apps.relational.client import service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_active_ta_topic_option_task(id, option_name, option_type, option_attrs, ta_topic_id, topic_id, client_id):
  log_message = ("Save ta topic option task for ta_topic_option_id: %s", id)

  with log_wrapper(logger.info, *log_message):
    return service.save_active_ta_topic_option(
        id, option_name, option_type, option_attrs, ta_topic_id, topic_id, client_id
    ).id


@job('high')
def save_active_client_task(id):
  log_message = ("client_id: %s", id)

  with log_wrapper(logger.info, *log_message):
    return service.save_active_client(id).id
