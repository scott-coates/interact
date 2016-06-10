from django.dispatch import receiver

from src.apps.engagement_discovery.signals import engagement_opportunity_discovered

# note: this is not a typical domain event. it is called in real-time and will not be persisted to the event store.
from src.domain.prospect import tasks
from src.domain.prospect.events import ProfileAddedToProspect1
from src.libs.common_domain.decorators import event_idempotent


@receiver(engagement_opportunity_discovered)
def created_from_engagement_opportunity_callback(sender, **kwargs):
  eo = kwargs['engagement_opportunity_discovery_object']

  prospect_task = tasks.save_prospect_from_engagement_discovery_task.delay(eo.provider_external_id, eo.provider_type)

  profile_task = tasks.save_profile_from_engagement_discovery_chain.delay(
      eo.provider_external_id, eo.provider_type, depends_on=prospect_task
  )

  tasks.save_engagement_opportunity_from_engagement_discovery_chain.delay(eo, depends_on=profile_task)


  # (
  #   prospect_tasks.save_prospect_from_provider_info_task.s(
  #       eo.provider_external_id,
  #       eo.provider_type
  #   )
  #   |
  #   profile_tasks.save_profile_from_provider_info_task.s(
  #       eo.provider_external_id,
  #       eo.provider_type
  #   )
  #   |
  #   engagement_opportunity_tasks.create_engagement_opportunity_task.s(eo)
  #   |
  #   engagement_opportunity_tasks.add_topic_to_engagement_opportunity_task.s(
  #       eo.topic_type
  #   )
  # ).delay()


@event_idempotent
@receiver(ProfileAddedToProspect1.event_signal)
def execute_added_profile_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']

  tasks.save_profile_lookup_by_provider_task.delay(
      event.id, event.provider_external_id,
      event.provider_type, aggregate_id
  )
