import logging

from django_rq import job

from src.apps.graph.topic import service

logger = logging.getLogger(__name__)


@job('high')
def create_topic_in_graphdb_task(topic_id):
  return service.create_topic_in_graphdb(topic_id)['id']
