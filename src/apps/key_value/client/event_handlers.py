from django.dispatch import receiver

from src.apps.key_value.client import tasks
from src.domain.client.events import ClientCreated1, ClientAssociatedWithTopic1
from src.domain.topic.events import TopicCreated1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ClientCreated1.event_signal)
def execute_client_created_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']

  tasks.save_active_client_task.delay(aggregate_id)


@event_idempotent
@receiver(TopicCreated1.event_signal)
def execute_topic_created_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']
  stem = event.snowball_stem
  tasks.save_client_topic_lookup_task.delay(aggregate_id, stem)


@event_idempotent
@receiver(ClientAssociatedWithTopic1.event_signal)
def execute_ta_topic_created_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']
  topic_id = event.topic_id
  tasks.save_client_topic_stem_task.delay(aggregate_id, topic_id)
