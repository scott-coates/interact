import logging

from django_rq import job

from src.apps.graph.prospect import services

logger = logging.getLogger(__name__)


@job('high')
def create_prospect_in_graphdb_task(prospect_id):
  return services.create_prospect_in_graphdb(prospect_id)['id']

@job('high')
def create_profile_in_graphdb_task(prospect_id, profile_id):
  return services.create_profile_in_graphdb(prospect_id, profile_id)['id']
