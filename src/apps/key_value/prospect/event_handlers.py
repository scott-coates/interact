from django.dispatch import receiver

from src.apps.key_value.prospect import tasks
from src.domain.prospect.events import TopicAddedToEngagementOpportunity1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(TopicAddedToEngagementOpportunity1.event_signal)
def execute_topic_added_eo_1(**kwargs):
  event = kwargs['event']

  tasks.save_eo_topic_set_task.delay(
      event.engagement_opportunity_id, event.topic_id
  )
