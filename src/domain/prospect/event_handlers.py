from django.dispatch import receiver

from src.apps.engagement_discovery.signals import engagement_opportunity_discovered
from src.domain.prospect import tasks
from src.domain.prospect.events import Prospect1AddedProfile, EngagementOpportunityAddedToProfile1
from src.libs.common_domain.decorators import event_idempotent


# note: this is not a typical domain event. it is called in real-time and will not be persisted to the event store.
@receiver(engagement_opportunity_discovered)
def created_from_engagement_opportunity_callback(sender, **kwargs):
  eo = kwargs['engagement_opportunity_discovery_object']

  prospect_task = tasks.populate_prospect_from_provider_info_task.delay(eo.profile_external_id, eo.provider_type)

  profile_task = tasks.populate_profile_from_provider_info_chain.delay(
      eo.profile_external_id, eo.provider_type, depends_on=prospect_task
  )

  eo_task = tasks.populate_engagement_opportunity_id_from_engagement_discovery_chain.delay(eo, depends_on=profile_task)

  tasks.add_topic_to_eo_chain.delay(eo.topic_id, depends_on=eo_task)

