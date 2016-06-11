import logging

from django_rq import job

from src.apps.graph.prospect import service

logger = logging.getLogger(__name__)


@job('high')
def create_prospect_in_graphdb_task(prospect_id):
  return service.create_prospect_in_graphdb(prospect_id)['id']


@job('high')
def create_profile_in_graphdb_task(prospect_id, profile_id):
  return service.create_profile_in_graphdb(prospect_id, profile_id)['id']


@job('high')
def create_eo_in_graphdb_task(profile_id, eo_id):
  return service.create_eo_in_graphdb(profile_id, eo_id)['id']


@job('high')
def add_topic_to_eo_in_graphdb_task(engagement_opportunity_id, topic_id):
  return service.add_topic_to_eo_in_graphdb(engagement_opportunity_id, topic_id)
