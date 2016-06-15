import logging

from django_rq import job

from src.apps.graph.client import service

logger = logging.getLogger(__name__)


@job('high')
def create_client_in_graphdb_task(client_id):
  return service.create_client_in_graphdb(client_id)['id']


@job('high')
def create_ta_topic_in_graphdb_task(client_id, ta_topic_id, topic_id):
  return service.create_ta_topic_in_graphdb(client_id, ta_topic_id, topic_id)['id']


@job('default')
def create_ea_in_graphdb_task(id, attrs, client_id):
  return service.create_ea_in_graphdb(id, attrs, client_id)['id']
