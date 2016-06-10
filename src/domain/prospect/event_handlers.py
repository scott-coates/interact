from django.dispatch import receiver

from src.apps.engagement_discovery.signals import engagement_opportunity_discovered

# note: this is not a typical domain event. it is called in real-time and will not be persisted to the event store.
from src.domain.prospect import tasks


@receiver(engagement_opportunity_discovered)
def created_from_engagement_opportunity_callback(sender, **kwargs):
  eo = kwargs['engagement_opportunity_discovery_object']

  prospect_task = tasks.save_prospect_from_provider_info_task.delay(eo.provider_external_id, eo.provider_type)

  profile_task = tasks.save_profile_from_provider_info_chain.delay(
      eo.provider_external_id, eo.provider_type, depends_on=prospect_task
  )


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
