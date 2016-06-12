import logging

from django_rq import job

from src.apps.graph.engagement_assignment import service

logger = logging.getLogger(__name__)


@job('high')
def create_ea_in_graphdb_task(id, attrs, client_id):
  return service.create_ea_in_graphdb(id, attrs, client_id)['id']
