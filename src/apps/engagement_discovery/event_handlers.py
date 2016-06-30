from django.dispatch import receiver

from src.apps.engagement_discovery import tasks
from src.domain.prospect.events import ProspectAddedProfile1


@receiver(ProspectAddedProfile1.event_signal)
def execute_prospect_added_profile_1(**kwargs):
  prospect_id = kwargs['aggregate_id']

  event = kwargs['event']
  external_id = event.external_id
  provider_type = event.provider_type

  tasks.discover_engagement_opportunities_from_profile_task.delay(external_id, provider_type, prospect_id)
