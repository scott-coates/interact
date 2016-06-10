import logging

from django_rq import job, get_queue
from rq import get_current_job

from src.domain.prospect import services
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('default')
def save_prospect_from_provider_info_task(provider_external_id, provider_type):
  log_message = ("provider_external_id: %s, provider_type: %s", provider_external_id, provider_type)

  with log_wrapper(logger.info, *log_message):
    return services.get_prospect_id_from_provider_info_(provider_external_id, provider_type).id


@job('default')
def save_profile_from_provider_info_chain(provider_external_id, provider_type):
  q = get_queue('default')
  job = get_current_job()
  first_job_id = job.dependencies[0].id
  first_job_result = q.fetch_job(first_job_id).result
  save_profile_from_provider_info_task(first_job_result, provider_external_id, provider_type)


@job('default')
def save_profile_from_provider_info_task(prospect_id, provider_external_id, provider_type):
  log_message = (
    "prospect_id: %s, provider_external_id: %s, provider_type: %s",
    prospect_id, provider_external_id, provider_type
  )

  with log_wrapper(logger.info, *log_message):
    return services.get_profile_id_from_provider_info(prospect_id, provider_external_id, provider_type).id
