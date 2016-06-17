import logging

from django_rq import job

from src.apps.graph.prospect import service

logger = logging.getLogger(__name__)


@job('default')
def create_prospect_in_graphdb_task(prospect_id):
  return service.create_prospect_in_graphdb(prospect_id)['id']


@job('default')
def delete_prospect_in_graphdb_task(prospect_id):
  return service.delete_prospect_in_graphdb(prospect_id)


@job('default')
def create_profile_in_graphdb_task(prospect_id, profile_id):
  return service.create_profile_in_graphdb(prospect_id, profile_id)['id']


@job('default')
def create_eo_in_graphdb_task(profile_id, eo_id):
  return service.create_eo_in_graphdb(profile_id, eo_id)['id']


@job('default')
def add_topic_to_eo_in_graphdb_task(engagement_opportunity_id, topic_id):
  try:
    ret_val = service.add_topic_to_eo_in_graphdb(engagement_opportunity_id, topic_id)
  except IndexError as e:

    raise Exception('Error adding topic to eo. EO was not listed as being deleted. Topic id: {0}. Eo id: {1}.'.
                    format(topic_id, engagement_opportunity_id)).with_traceback(e.__traceback__)

  return ret_val
