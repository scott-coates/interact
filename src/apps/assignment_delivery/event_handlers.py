from django.dispatch import receiver

from src.apps.assignment_delivery import tasks
from src.domain.client.events import ClientProcessedEngagementAssignmentBatch1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ClientProcessedEngagementAssignmentBatch1.event_signal)
def execute_ea_created_1(**kwargs):
  event = kwargs['event']

  batch_eas = event.assigned

  for ea in batch_eas:
    tasks.deliver_ea_task.delay(ea)
