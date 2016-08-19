import logging

from django_rq import job

from src.apps.read_model.key_value.client import service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('high')
def save_active_client_task(id):
  log_message = ("client_id: %s", id)

  with log_wrapper(logger.info, *log_message):
    return service.save_active_client(id)


@job('default')
def save_client_assigned_prospect_task(client_id, prospect_id):
  log_message = ("client_id: %s prospect_id: %s", client_id, prospect_id)

  with log_wrapper(logger.info, *log_message):
    return service.save_client_assigned_prospect(client_id, prospect_id)


@job('default')
def clear_ea_batch_to_be_processed_task(client_id, batch_id):
  return service.clear_ea_batch_to_be_processed(client_id, batch_id)


@job('default')
def save_client_recent_engagement_assignment_scores_task(client_id, batch_eas):
  for ea in batch_eas:
    service.save_client_recent_engagement_assignment_scores(client_id, ea)
