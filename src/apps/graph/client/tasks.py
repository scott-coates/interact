import logging

from django_rq import job

from src.apps.graph.client import service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def create_client_in_graphdb_task(client_id):
  log_message = (
    "client_id: %s",
    client_id
  )
  with log_wrapper(logger.info, *log_message):
    return service.create_client_in_graphdb(client_id)['id']


@job('high')
def create_ta_topic_in_graphdb_task(client_id, ta_topic_id, relevance, topic_id):
  log_message = (
    "client_id: %s, topic_id: %s",
    client_id, topic_id
  )
  with log_wrapper(logger.info, *log_message):
    return service.create_ta_topic_in_graphdb(client_id, ta_topic_id, relevance, topic_id)['id']


@job('default')
def create_ea_in_graphdb_task(id, attrs, client_id):
  log_message = (
    "ea_id: %s, client_id: %s",
    id, client_id
  )
  with log_wrapper(logger.info, *log_message):
    return service.create_ea_in_graphdb(id, attrs, client_id)['id']
