import logging

from django_rq import job
from rq import get_current_job

from src.apps.key_value.prospect.service import eo_contains_topic
from src.domain.prospect import service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


# the reason we're doing these result_ttl=-1 and job.delete() everywhere is because by default, rq only keeps results
# for about 500 seconds and these jobs depend on each other. So sometimes they don't run for more than 500 seconds
# in between dependencies. So keep the jobs around forever and when a dependent job runs, it'll delete it's parent task.

@job('default', result_ttl=-1)
def populate_prospect_from_provider_info_task(external_id, provider_type):
  log_message = ("external_id: %s, provider_type: %s", external_id, provider_type)

  with log_wrapper(logger.info, *log_message):
    return service.populate_prospect_id_from_provider_info_(external_id, provider_type)


@job('default', result_ttl=-1)
def populate_profile_from_provider_info_task(external_id, provider_type):
  job = get_current_job()

  prospect_id = job.dependency.result

  log_message = (
    "prospect_id: %s, external_id: %s, provider_type: %s",
    prospect_id, external_id, provider_type
  )

  with log_wrapper(logger.info, *log_message):
    ret_val = service.populate_profile_id_from_provider_info(prospect_id, external_id, provider_type)

    job.dependency.delete()

    return ret_val


@job('default', result_ttl=-1)
def populate_engagement_opportunity_id_from_engagement_discovery_task(engagement_opportunity_discovery_object):
  job = get_current_job()
  profile_id = job.dependency.result

  log_message = (
    "Begin add eo. profile_id: %s, eo_external_id: %s",
    profile_id, engagement_opportunity_discovery_object.engagement_opportunity_external_id
  )

  with log_wrapper(logger.info, *log_message):
    ret_val = service.populate_engagement_opportunity_id_from_engagement_discovery(profile_id,
                                                                                   engagement_opportunity_discovery_object)
    job.dependency.delete()
    return ret_val


@job('default')
def add_topic_to_eo_task(topic_id):
  job = get_current_job()
  eo_id = job.dependency.result
  log_message = (
    "eo_id: %s, topic_id: %s",
    eo_id, topic_id
  )

  with log_wrapper(logger.info, *log_message):
    ret_val = None

    if not eo_contains_topic(eo_id, topic_id):
      ret_val = service.add_topic_to_eo(eo_id, topic_id)

    job.dependency.delete()

    return ret_val
