from django.dispatch import receiver

from src.apps.engagement_discovery.signals import engagement_opportunity_discovered
from src.domain.prospect import tasks
from src.domain.prospect.events import duplicate_profile_discovered, ProspectMarkedAsDuplicate, \
  EngagementOpportunityAddedToProfile1
from src.domain.prospect.tasks import handle_duplicate_profile_task


@receiver(engagement_opportunity_discovered)
def created_from_engagement_opportunity_callback(sender, **kwargs):
  eo = kwargs['engagement_opportunity_discovery_object']

  tasks.populate_prospect_from_provider_info_chain.delay(eo.profile_external_id, eo.provider_type, eo)


# note: this is not a typical domain event. it is called in real-time and will not be persisted to the event store.
@receiver(duplicate_profile_discovered)
def handle_duplicate_profile(sender, **kwargs):
  duplicate_prospect_id = kwargs['duplicate_prospect_id']
  existing_external_id = kwargs['existing_external_id']
  existing_provider_type = kwargs['existing_provider_type']

  handle_duplicate_profile_task.delay(duplicate_prospect_id, existing_external_id, existing_provider_type)


@receiver(ProspectMarkedAsDuplicate.event_signal)
@receiver(EngagementOpportunityAddedToProfile1.event_signal)
def execute_prospect_duplicate_1(**kwargs):
  duplicate_prospect_id = kwargs['aggregate_id']
  event = kwargs['event']
  existing_prospect_id = event.existing_prospect_id
  if existing_prospect_id:
    tasks.consume_duplicate_prospect_task.delay(existing_prospect_id, duplicate_prospect_id)
