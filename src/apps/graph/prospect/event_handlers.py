from django.dispatch import receiver

from src.apps.graph.prospect import tasks
from src.domain.prospect.events import ProspectCreated1, ProfileAddedToProspect1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ProspectCreated1.event_signal)
def add_client(**kwargs):
  prospect_id = kwargs['aggregate_id']
  tasks.create_prospect_in_graphdb_task.delay(prospect_id)


@event_idempotent
@receiver(ProfileAddedToProspect1.event_signal)
def add_profile(**kwargs):
  prospect_id = kwargs['aggregate_id']
  event = kwargs['event']
  profile_id = event.id
  tasks.create_profile_in_graphdb_task.delay(prospect_id, profile_id)
