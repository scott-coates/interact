from django.dispatch import receiver

from src.apps.engagement_discovery import tasks
from src.domain.prospect.events import ProspectAddedProfile1


@receiver(ProspectAddedProfile1.event_signal)
def execute_prospect_added_profile_1(**kwargs):
  prospect_id = kwargs['aggregate_id']
  event = kwargs['event']
