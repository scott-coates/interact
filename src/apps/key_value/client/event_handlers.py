from django.dispatch import receiver

from src.apps.key_value.client import tasks
from src.domain.client.events import ClientCreated1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ClientCreated1.event_signal)
def execute_client_created_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']

  tasks.save_active_client_task.delay(aggregate_id)
