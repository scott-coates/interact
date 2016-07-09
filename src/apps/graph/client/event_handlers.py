from django.dispatch import receiver

from src.apps.graph.client import tasks
from src.domain.client.events import ClientCreated1, ClientAssociatedWithTopic1, \
  ClientProcessedEngagementAssignmentBatch1
from src.domain.common import constants
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
  relevance = event.relevance
  topic_id = event.topic_id
  tasks.create_ta_topic_in_graphdb_task.delay(client_id, ta_topic_id, relevance, topic_id)


@event_idempotent
@receiver(ClientProcessedEngagementAssignmentBatch1.event_signal)
def execute_ea_created_1(**kwargs):
  client_id = kwargs['aggregate_id']

  event = kwargs['event']

  batch_eas = event.skipped + event.assigned

  for ea in batch_eas:
    tasks.create_ea_in_graphdb_task.delay(ea[constants.ID], ea[constants.ATTRS], client_id)
