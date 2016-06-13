import logging

from django_rq import job

from src.apps.relational.client import service as relational_client_service
from src.domain.client import service as client_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('default')
def refresh_assignments_for_clients_task():
  active_clients = relational_client_service.get_active_clients()

  for client in active_clients:
    refresh_assignments_for_client_task.delay(client.id)


@job('default')
def refresh_assignments_for_client_task(client_id):
  log_message = (
    "Refresh assignments task for client_id: %s",
    client_id
  )

  with log_wrapper(logger.debug, *log_message):
    ret_val = client_service.refresh_assignments(client_id)

  return ret_val
