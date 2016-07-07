import logging

from django_rq import job

from src.domain.client import service as client_service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('default')
def refresh_assignments_for_clients_task():
  active_clients_ids = client_service.get_active_client_ids()

  for client_ids in active_clients_ids:
    refresh_assignments_for_client_task.delay(client_ids)


@job('default')
def refresh_assignments_for_client_task(client_id):
  log_message = (
    "Refresh assignments task for client_id: %s",
    client_id
  )

  with log_wrapper(logger.debug, *log_message):
    entities_to_add = client_service.get_unassigned_grouped_entities_for_client(client_id)

    counter = 1
    total_assignments_count = len(entities_to_add)

    assign_log_message = ("Assignments to create for client_id: %s: %i", client_id, total_assignments_count)

    with log_wrapper(logger.debug, *assign_log_message):
      for group in entities_to_add:
        group_log_message = ("Issued task for assignment: %i out of %i for client_id: %s", counter,
                             total_assignments_count,
                             client_id)

        with log_wrapper(logger.debug, *group_log_message):
          refresh_assignment_for_client_task.delay(client_id, group, counter, total_assignments_count)
          counter += 1


@job('default')
def refresh_assignment_for_client_task(client_id, assignment_group, counter, total_assignments_count):
  group_log_message = ("Assignment: %i out of %i for client_id: %s", counter, total_assignments_count, client_id)
  with log_wrapper(logger.debug, *group_log_message):
    client_service.refresh_assignments(client_id, assignment_group)
