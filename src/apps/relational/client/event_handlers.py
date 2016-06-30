from django.dispatch import receiver

from src.apps.relational.client import tasks
from src.domain.client.events import ClientAddedTargetAudienceTopicOption1, ClientCreated1, ClientAssociatedWithTopic1
from src.domain.prospect.events import ProspectCreated1, ProspectAddedProfile1, EngagementOpportunityAddedToProfile1, \
  ProspectUpdatedAttrsFromProfile1, TopicAddedToEngagementOpportunity1, ProspectDeleted
from src.domain.topic.events import TopicCreated1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ClientAddedTargetAudienceTopicOption1.event_signal)
def execute_added_target_audience_topic_option_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']

  tasks.save_active_ta_topic_option_task.delay(
      event.id, event.name,
      event.type, event.attrs, event.ta_topic_id, event.ta_topic_relevance,
      event.topic_id, aggregate_id
  )


@event_idempotent
@receiver(ClientCreated1.event_signal)
def execute_client_created_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']

  tasks.save_client_ea_lookup_task.delay(
      aggregate_id, event.ta_attrs
  )


@event_idempotent
@receiver(ClientAssociatedWithTopic1.event_signal)
def execute_ta_topic_created_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']
  relevance = event.relevance
  topic_id = event.topic_id
  tasks.save_topic_to_client_ea_lookup_task.delay(aggregate_id, relevance, topic_id)


@event_idempotent
@receiver(ProspectCreated1.event_signal)
@receiver(ProspectUpdatedAttrsFromProfile1.event_signal)
def execute_added_prospect_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']

  tasks.save_prospect_ea_lookup_task.delay(aggregate_id, event.attrs)


@event_idempotent
@receiver(ProspectDeleted.event_signal)
def execute_deleted_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']

  tasks.delete_prospect_for_ea_task.delay(aggregate_id)


@event_idempotent
@receiver(ProspectAddedProfile1.event_signal)
def execute_added_profile_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']

  tasks.save_profile_ea_lookup_task.delay(event.id, event.attrs, event.provider_type, aggregate_id)


@event_idempotent
@receiver(EngagementOpportunityAddedToProfile1.event_signal)
def execute_added_eo_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']

  tasks.save_eo_ea_lookup_task.delay(event.id, event.attrs, event.provider_type, event.profile_id, aggregate_id)


@event_idempotent
@receiver(TopicAddedToEngagementOpportunity1.event_signal)
def execute_added_topic_to_eo_1(**kwargs):
  event = kwargs['event']

  eo_id = event.engagement_opportunity_id
  topic_id = event.topic_id

  tasks.save_topic_to_eo_ea_lookup_task.delay(eo_id, topic_id)
