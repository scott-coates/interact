import logging

from django_rq import job
from rq import get_current_job

from src.domain.prospect import service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('default')
def populate_prospect_from_provider_info_task(profile_external_id, provider_type):
  log_message = ("profile_external_id: %s, provider_type: %s", profile_external_id, provider_type)

  with log_wrapper(logger.info, *log_message):
    return service.populate_prospect_id_from_provider_info_(profile_external_id, provider_type)


@job('default')
def populate_profile_from_provider_info_chain(profile_external_id, provider_type):
  job = get_current_job()
  prospect_id = job.dependency.result
  # queue up this job now because we want to store the prospect id (result of previous job) before that job's TTL
  # expires
  populate_profile_from_provider_info_task.delay(prospect_id, profile_external_id, provider_type)


@job('default')
def populate_profile_from_provider_info_task(prospect_id, profile_external_id, provider_type):
  log_message = (
    "prospect_id: %s, profile_external_id: %s, provider_type: %s",
    prospect_id, profile_external_id, provider_type
  )

  with log_wrapper(logger.info, *log_message):
    return service.populate_profile_id_from_provider_info(prospect_id, profile_external_id, provider_type)


@job('default')
def populate_engagement_opportunity_id_from_engagement_discovery_chain(engagement_opportunity_discovery_object):
  job = get_current_job()
  profile_id = job.dependency.result
  # queue up this job now because we want to store the prospect id (result of previous job) before that job's TTL
  # expires
  populate_engagement_opportunity_id_from_engagement_discovery_task.delay(profile_id, engagement_opportunity_discovery_object)


@job('default')
def populate_engagement_opportunity_id_from_engagement_discovery_task(profile_id, engagement_opportunity_discovery_object):
  log_message = (
    "Begin add eo. profile_id: %s, eo_external_id: %s",
    profile_id, engagement_opportunity_discovery_object.engagement_opportunity_external_id
  )

  with log_wrapper(logger.info, *log_message):
    return service.populate_engagement_opportunity_id_from_engagement_discovery(profile_id,
                                                                                engagement_opportunity_discovery_object)


@job('high')
def save_profile_lookup_by_provider_task(profile_id, profile_external_id, provider_type, prospect_id):
  log_message = (
    "profile_id: %s, profile_external_id: %s, provider_type: %s",
    prospect_id, profile_external_id, provider_type
  )

  with log_wrapper(logger.info, *log_message):
    return service.save_profile_lookup_by_provider(profile_id, profile_external_id, provider_type, prospect_id)
