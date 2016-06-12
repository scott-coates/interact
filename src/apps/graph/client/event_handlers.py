from django.dispatch import receiver

from src.apps.graph.client import tasks
from src.domain.client.events import ClientCreated1, ClientAssociatedWithTopic1, ClientAddedEngagementAssignment1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ClientCreated1.event_signal)
def add_client(**kwargs):
  client_id = kwargs['aggregate_id']
  tasks.create_client_in_graphdb_task.delay(client_id)


@event_idempotent
@receiver(ClientAssociatedWithTopic1.event_signal)
def add_ta_topic(**kwargs):
  client_id = kwargs['aggregate_id']
  event = kwargs['event']
  ta_topic_id = event.id
  topic_id = event.topic_id
  tasks.create_ta_topic_in_graphdb_task.delay(client_id, ta_topic_id, topic_id)


@event_idempotent
@receiver(ClientAddedEngagementAssignment1.event_signal)
def execute_ea_created_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  tasks.create_ea_in_graphdb_task.delay(aggregate_id)
