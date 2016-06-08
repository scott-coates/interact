import logging

from django_rq import job

from src.apps.graph.client import services

logger = logging.getLogger(__name__)


@job('high')
def create_client_in_graphdb_task(client_id):
  return services.create_client_in_graphdb(client_id)['id']

@job('high')
def create_ta_topic_in_graphdb_task(client_id, ta_topic_id, topic_id):
  # todo should we add retry logic here?
  return services.create_ta_topic_in_graphdb(client_id, ta_topic_id, topic_id)['id']
