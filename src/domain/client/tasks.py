import logging
from datetime import timedelta

import django_rq
from django_rq import job

from src.apps.read_model.graph.client.service import get_unassigned_grouped_entities_for_client_from_graphdb
from src.apps.read_model.key_value.client.service import mark_ea_batch_to_be_processed, get_active_client_ids, \
  get_ea_batch_to_be_processed
from src.apps.read_model.relational.client.service import get_assignment_batch_processed_count
from src.domain.client import service as client_service
from src.libs.python_utils.id.id_utils import generate_id
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('default')
def refresh_assignments_for_clients_task():
  active_clients_ids = get_active_client_ids()

  for client_ids in active_clients_ids:
    refresh_assignments_for_client_task.delay(client_ids)


@job('default')
def refresh_assignments_for_client_task(client_id):
  log_message = (
    "Refresh assignments task for client_id: %s",
    client_id
  )

  with log_wrapper(logger.debug, *log_message):
    entities_to_add = get_unassigned_grouped_entities_for_client_from_graphdb(client_id)
  total_assignments_count = len(entities_to_add)
  if total_assignments_count:
    batch_id = generate_id()
    counter = 1

    assign_log_message = ("Assignments to create for client_id: %s: batch_id: %s count: %i", client_id, batch_id,
                          total_assignments_count)

    with log_wrapper(logger.debug, *assign_log_message):

      mark_ea_batch_to_be_processed(client_id, batch_id, total_assignments_count)
      logger.debug('Marked group to be processed client_id: %s batch_id: %s', client_id, batch_id)

      for group in entities_to_add:
        group_log_message = ("Issued task for assignment: %i out of %i for client_id: %s", counter,
                             total_assignments_count,
                             client_id)

        with log_wrapper(logger.debug, *group_log_message):
          save_assignment_batch_from_attrs_task.delay(client_id, batch_id, group, counter, total_assignments_count)
          counter += 1

    # process the batch once it's all done
    _enqueue_assignment_check_(client_id, batch_id)


@job('default')
def save_assignment_batch_from_attrs_task(client_id, batch_id, assignment_group, counter, total_assignments_count):
  group_log_message = ("Assignment: %i out of %i for client_id: %s", counter, total_assignments_count, client_id)
  with log_wrapper(logger.debug, *group_log_message):
    client_service.save_assignment_batch_from_attrs(client_id, assignment_group, batch_id, counter)


@job('default')
def process_assignment_batch_task(client_id, batch_id):
  group_log_message = ('Checking to process batch. client: %s, batch: %s', client_id, batch_id)
  with log_wrapper(logger.debug, *group_log_message):
    expected_count = get_ea_batch_to_be_processed(client_id, batch_id)
    actual_count = get_assignment_batch_processed_count(client_id, batch_id)

    if expected_count == actual_count:
      process_log_message = ('Batch is complete. Starting to process. Count: %i', actual_count)

      with log_wrapper(logger.debug, *process_log_message):
        client_service.process_assignment_batch(client_id, batch_id)
    else:
      logger.debug('Batch not complete yet. Actual: %i, Expected: %i', actual_count, expected_count)
      _enqueue_assignment_check_(client_id, batch_id)


def _enqueue_assignment_check_(client_id, batch_id):
  scheduler = django_rq.get_scheduler('default')
  # delay this task so that we have time to check if it's a duplicate prospect before we proceed
  scheduler.enqueue_in(timedelta(minutes=1), process_assignment_batch_task, client_id, batch_id)
