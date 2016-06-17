from django.dispatch import receiver

from src.apps.graph.prospect import tasks
from src.domain.prospect.events import ProspectCreated1, ProspectAddedProfile1, \
  EngagementOpportunityAddedToProfile1, TopicAddedToEngagementOpportunity1, ProspectDeleted
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ProspectCreated1.event_signal)
def add_client(**kwargs):
  prospect_id = kwargs['aggregate_id']
  tasks.create_prospect_in_graphdb_task.delay(prospect_id)


@event_idempotent
@receiver(ProspectDeleted.event_signal)
def delete_client(**kwargs):
  prospect_id = kwargs['aggregate_id']
  tasks.delete_prospect_in_graphdb_task.delay(prospect_id)


@event_idempotent
@receiver(ProspectAddedProfile1.event_signal)
def add_profile(**kwargs):
  prospect_id = kwargs['aggregate_id']
  event = kwargs['event']
  profile_id = event.id
  tasks.create_profile_in_graphdb_task.delay(prospect_id, profile_id)


@event_idempotent
@receiver(EngagementOpportunityAddedToProfile1.event_signal)
def add_eo(**kwargs):
  event = kwargs['event']
  eo_id = event.id
  profile_id = event.profile_id
  tasks.create_eo_in_graphdb_task.delay(profile_id, eo_id)


@event_idempotent
@receiver(TopicAddedToEngagementOpportunity1.event_signal)
def add_topic_to_eo(**kwargs):
  prospect_id = kwargs['aggregate_id']
  event = kwargs['event']
  eo_id = event.engagement_opportunity_id
  topic_id = event.topic_id
  tasks.add_topic_to_eo_in_graphdb_task.delay(prospect_id, eo_id, topic_id)
