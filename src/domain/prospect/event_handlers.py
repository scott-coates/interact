from django.dispatch import receiver

from src.apps.engagement_discovery.signals import engagement_opportunity_discovered
from src.domain.prospect import tasks
from src.domain.prospect.events import duplicate_profile_discovered


@receiver(engagement_opportunity_discovered)
def created_from_engagement_opportunity_callback(sender, **kwargs):
  eo = kwargs['engagement_opportunity_discovery_object']

  prospect_task = tasks.populate_prospect_from_provider_info_task.delay(eo.profile_external_id, eo.provider_type)

  profile_task = tasks.populate_profile_from_provider_info_task.delay(eo.profile_external_id, eo.provider_type,
                                                                      depends_on=prospect_task)

  eo_task = tasks.populate_engagement_opportunity_id_from_engagement_discovery_task.delay(eo, depends_on=profile_task)

  tasks.add_topic_to_eo_task.delay(eo.topic_id, depends_on=eo_task)


# note: this is not a typical domain event. it is called in real-time and will not be persisted to the event store.
@receiver(duplicate_profile_discovered)
def handle_duplicate_profile(sender, **kwargs):
  duplicate_prospect_id = kwargs['duplicate_prospect_id']
  existing_external_id = kwargs['existing_external_id']
  existing_provider_type = kwargs['existing_provider_type']
