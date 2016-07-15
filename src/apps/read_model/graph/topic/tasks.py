import logging

from django_rq import job

from src.apps.read_model.graph.topic import service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def create_topic_in_graphdb_task(topic_id):
  log_message = (
    "topic_id: %s",
    topic_id
  )
  with log_wrapper(logger.info, *log_message):
    return service.create_topic_in_graphdb(topic_id)['id']
