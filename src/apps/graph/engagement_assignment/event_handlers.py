from django.dispatch import receiver

from src.apps.graph.engagement_assignment import tasks
from src.domain.engagement_assignment.events import EngagementAssignmentCreated1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(EngagementAssignmentCreated1.event_signal)
def execute_ea_created_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  tasks.create_ea_in_graphdb_task.delay(aggregate_id)
