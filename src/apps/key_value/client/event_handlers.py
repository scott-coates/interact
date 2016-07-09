from django.dispatch import receiver

from src.apps.key_value.client import tasks
from src.domain.client.events import ClientCreated1, ClientProcessedEngagementAssignmentBatch1
from src.domain.common import constants
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ClientCreated1.event_signal)
def execute_client_created_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']

  tasks.save_active_client_task.delay(aggregate_id)


@event_idempotent
@receiver(ClientProcessedEngagementAssignmentBatch1.event_signal)
def execute_ea_created_1(**kwargs):
  client_id = kwargs['aggregate_id']

  event = kwargs['event']

  for ea in event.assigned:
    tasks.save_client_assigned_prospect_task.delay(client_id, ea[constants.PROSPECT_ID])


@event_idempotent
@receiver(ClientProcessedEngagementAssignmentBatch1.event_signal)
def execute_ea_processed_1(**kwargs):
  client_id = kwargs['aggregate_id']

  event = kwargs['event']
  batch_id = event.batch_id

  tasks.clear_ea_batch_to_be_processed_task.delay(client_id, batch_id)
