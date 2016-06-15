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


@job('high')
def save_client_topic_lookup_task(id, stem):
  log_message = ("topic_id: %s stem: %s", id, stem)

  with log_wrapper(logger.info, *log_message):
    return service.save_client_topic_lookup(id, stem)


@job('high')
def save_client_topic_stem_task(id, topic_id):
  log_message = ("client_id: %s topic_id: %s", id, topic_id)

  with log_wrapper(logger.info, *log_message):
    return service.save_client_topic_stem(id, topic_id)
