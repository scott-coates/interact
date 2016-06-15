from django.dispatch import receiver

from src.apps.key_value.client import tasks
from src.domain.client.events import ClientCreated1, ClientAddedEngagementAssignment1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ClientCreated1.event_signal)
def execute_client_created_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']

  tasks.save_active_client_task.delay(aggregate_id)


@event_idempotent
@receiver(ClientAddedEngagementAssignment1.event_signal)
def execute_ea_created_1(**kwargs):
  client_id = kwargs['aggregate_id']

  event = kwargs['event']

  prospect_id = event.prospect_id

  tasks.save_client_assigned_prospect_task.delay(client_id, prospect_id)
