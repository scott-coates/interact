import logging

from django_rq import job

from src.apps.key_value.client import service as kv_client_service
from src.domain.client import service as client_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('default')
def refresh_assignments_for_clients_task():
  active_clients_ids = kv_client_service.get_active_client_ids()

  for client_ids in active_clients_ids:
    refresh_assignments_for_client_task.delay(client_ids)


@job('default')
def refresh_assignments_for_client_task(client_id):
  log_message = (
    "Refresh assignments task for client_id: %s",
    client_id
  )

  with log_wrapper(logger.debug, *log_message):
    ret_val = client_service.refresh_assignments(client_id)

  return ret_val
