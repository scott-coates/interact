from django.dispatch import receiver

from src.apps.graph.client import tasks
from src.domain.client.events import ClientCreated1, AssociatedWithTopic1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ClientCreated1.event_signal)
def add_client(**kwargs):
  client_id = kwargs['aggregate_id']
  tasks.create_client_in_graphdb_task.delay(client_id)


@event_idempotent
@receiver(AssociatedWithTopic1.event_signal)
def add_ta_topic(**kwargs):
  client_id = kwargs['aggregate_id']
  event = kwargs['event']
  ta_topic_id = event.id
  topic_id = event.topic_id
  tasks.create_ta_topic_in_graphdb_task.delay(client_id, ta_topic_id, topic_id)

#
# @event_idempotent
# @receiver(created)
# def topic_created_callback(**kwargs):
#   tasks.create_topic_in_graphdb_task.delay(kwargs['topic_uid'])
#
#
# @event_idempotent
# @receiver(deleted)
# def topic_deleted_callback(**kwargs):
#   tasks.delete_topic_in_graphdb_task.delay(kwargs['topic_uid'])
#
#
# @event_idempotent
# @receiver(added_subtopic)
# def subtopic_created_callback(**kwargs):
#   tasks.create_subtopic_in_graphdb_task.delay(kwargs['topic_uid'], kwargs['subtopic_uid'])
#
#
# @event_idempotent
# @receiver(removed_subtopic)
# def subtopic_removed_callback(**kwargs):
#   tasks.remove_subtopic_in_graphdb_task.delay(kwargs['topic_uid'], kwargs['subtopic_uid'])
