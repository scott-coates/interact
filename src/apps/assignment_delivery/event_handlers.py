from django.dispatch import receiver

from src.apps.assignment_delivery import tasks
from src.domain.client.events import ClientProcessedEngagementAssignmentBatch1
from src.libs.common_domain.decorators import event_idempotent


# @event_idempotent
# @receiver(ClientProcessedEngagementAssignmentBatch1.event_signal)
def execute_ea_created_1(**kwargs):
  event = kwargs['event']

  batch_eas = event.assigned

  for ea in batch_eas:
    tasks.deliver_ea_to_analytics_service_task.delay(ea)


@event_idempotent
@receiver(ClientProcessedEngagementAssignmentBatch1.event_signal)
def execute_ea_created_1_for_model(**kwargs):
  event = kwargs['event']

  batch_eas = event.assigned
  batch_id = event.batch_id

  for ea in batch_eas:
    tasks.deliver_ea_to_read_model_task.delay(ea, batch_id)
