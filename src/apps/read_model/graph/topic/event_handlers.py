from django.dispatch import receiver

from src.apps.read_model.graph.topic import tasks
from src.domain.topic.events import TopicCreated1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(TopicCreated1.event_signal)
def execute_added_target_audience_topic_option_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  tasks.create_topic_in_graphdb_task.delay(aggregate_id)
