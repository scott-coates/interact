from django.dispatch import receiver

from src.apps.read_model.key_value.prospect import tasks
from src.domain.common import constants
from src.domain.prospect.events import ProspectDeleted1, EngagementOpportunityAddedToProfile1
from src.libs.common_domain.decorators import event_idempotent


@event_idempotent
@receiver(ProspectDeleted1.event_signal)
def execute_prospect_deleted_1(**kwargs):
  pass


@event_idempotent
@receiver(EngagementOpportunityAddedToProfile1.event_signal)
def execute_added_eo_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']

  attrs = event.attrs

  text = attrs.get(constants.TEXT)

  if text:
    tasks.save_recent_eo_content_task.delay(
        event.id, text, event.external_id,
        event.provider_type, event.provider_action_type, aggregate_id
    )


@event_idempotent
@receiver(EngagementOpportunityAddedToProfile1.event_signal)
def execute_added_eo_save_discovery_network_1(**kwargs):
  aggregate_id = kwargs['aggregate_id']
  event = kwargs['event']

  attrs = event.attrs

  mentions = attrs.get(constants.MENTIONS)

  if mentions:
    provider_type = event.provider_type
    prospect_id = aggregate_id

    for mention in mentions:
      external_id = mention[constants.EXTERNAL_ID]

      tasks.save_recent_prospect_discovery_network_connection_task.delay(
          external_id, provider_type, prospect_id
      )
