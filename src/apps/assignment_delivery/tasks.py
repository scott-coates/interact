import logging

from django_rq import job
from outliers import smirnov_grubbs as grubbs

from src.apps.assignment_delivery.service import deliver_ea
from src.apps.relational.client.service import delete_ea_deliver
from src.domain.client import service as client_service
from src.domain.common import constants

logger = logging.getLogger(__name__)


@job('default')
def deliver_assignments_for_clients_task():
  deliver_clients_ids = client_service.get_client_ids_ready_for_delivery()

  for client_id in deliver_clients_ids:
    deliver_assignments_for_client_task.delay(client_id)


@job('default')
def deliver_assignments_for_client_task(client_id):
  delivery_data = client_service.get_delivery_data_by_client_id(client_id)

  scores = [d[constants.SCORE] for d in delivery_data]

  accepted = grubbs.test(scores, 0.05)

  for delivery in delivery_data:
    ea_id = delivery[constants.ID]

    score = delivery[constants.SCORE]
    should_deliver = score in accepted

    deliver = None
    if should_deliver:
      deliver = deliver_ea_task.delay(ea_id)

    delete_ea_deliver_task.delay(ea_id, depends_on=deliver)


@job('default')
def deliver_ea_task(ea_id):
  return deliver_ea(ea_id)


@job('default')
def delete_ea_deliver_task(ea_id):
  return delete_ea_deliver(ea_id)
