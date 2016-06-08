from django.dispatch import receiver

from src.apps.graph.topic import tasks
from src.domain.topic.events import TopicCreated1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(TopicCreated1.event_signal)
def execute_added_topic_option_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  tasks.create_topic_in_graphdb_task.delay(aggregate_id)

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
