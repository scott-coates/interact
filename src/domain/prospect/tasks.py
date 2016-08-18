import logging

from django_rq import job

from src.domain.prospect import service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


# we cannot use rq job dependencies because rq-retry uses rq-scheduler which doesn't respect job dependencies.
# this is a hack to get around that.

@job('default')
def populate_prospect_from_provider_info_chain(external_id, provider_type,
                                               engagement_opportunity_discovery_object=None):
  log_message = ("external_id: %s, provider_type: %s", external_id, provider_type)

  with log_wrapper(logger.info, *log_message):
    prospect_id = service.populate_prospect_id_from_provider_info_(external_id, provider_type)
    populate_profile_from_provider_info_chain.delay(prospect_id, external_id, provider_type,
                                                    engagement_opportunity_discovery_object)


@job('default')
def populate_profile_from_provider_info_chain(prospect_id, external_id, provider_type,
                                              engagement_opportunity_discovery_object):
  log_message = (
    "prospect_id: %s, external_id: %s, provider_type: %s",
    prospect_id, external_id, provider_type
  )

  with log_wrapper(logger.info, *log_message):
    profile_id = service.populate_profile_id_from_provider_info(prospect_id, external_id, provider_type)

    # this is why we're explicitly naming the method `chain` because rq-scheduler doesn't support chaining tasks
    if engagement_opportunity_discovery_object:
      populate_engagement_opportunity_id_from_engagement_discovery_task.delay(profile_id, prospect_id,
                                                                              engagement_opportunity_discovery_object)


@job('default')
def populate_engagement_opportunity_id_from_engagement_discovery_task(profile_id, prospect_id,
                                                                      engagement_opportunity_discovery_object):
  log_message = (
    "Begin add eo. profile_id: %s, eo_external_id: %s",
    profile_id, engagement_opportunity_discovery_object.engagement_opportunity_external_id
  )

  with log_wrapper(logger.info, *log_message):
    ret_val = service.populate_engagement_opportunity_id_from_engagement_discovery(profile_id, prospect_id,
                                                                                   engagement_opportunity_discovery_object)
    return ret_val


@job('default')
def handle_duplicate_profile_task(duplicate_prospect_id, existing_external_id, existing_provider_type):
  log_message = (
    "duplicate_prospect_id: %s, existing_external_id: %s existing_provider_type: %s",
    duplicate_prospect_id, existing_external_id, existing_provider_type
  )

  with log_wrapper(logger.info, *log_message):
    ret_val = service.handle_duplicate_profile(duplicate_prospect_id, existing_external_id,
                                               existing_provider_type)

    return ret_val


@job('default')
def consume_duplicate_prospect_task(existing_prospect_id, duplicate_prospect_id):
  log_message = (
    "existing_prospect_id: %s, duplicate_prospect_id: %s",
    existing_prospect_id, duplicate_prospect_id
  )

  with log_wrapper(logger.info, *log_message):
    ret_val = service.consume_duplicate_prospect(existing_prospect_id, duplicate_prospect_id)

    return ret_val
