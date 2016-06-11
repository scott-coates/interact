from django.dispatch import receiver

from src.apps.relational.prospect import tasks
from src.domain.prospect.events import EngagementOpportunityAddedToProfile1, Prospect1AddedProfile
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(Prospect1AddedProfile.event_signal)
def execute_added_profile_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']

  tasks.save_profile_lookup_by_provider_task.delay(
      event.id, event.external_id,
      event.provider_type, aggregate_id
  )


@event_idempotent
@receiver(EngagementOpportunityAddedToProfile1.event_signal)
def execute_added_eo_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']

  tasks.save_eo_lookup_by_provider_task.delay(
      event.id, event.external_id,
      event.provider_type, aggregate_id
  )
