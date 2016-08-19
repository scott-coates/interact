from datetime import timedelta

import django_rq
from django.dispatch import receiver

from src.apps.engagement_discovery import tasks
from src.domain.client.events import ClientProcessedEngagementAssignmentBatch1
from src.domain.prospect.events import ProspectAddedProfile1


@receiver(ProspectAddedProfile1.event_signal)
def execute_prospect_added_profile_1(**kwargs):
  scheduler = django_rq.get_scheduler('default')

  prospect_id = kwargs['aggregate_id']

  event = kwargs['event']

  if not event.is_restricted:
    external_id = event.external_id
    provider_type = event.provider_type

    # delay this task so that we have time to check if it's a duplicate prospect before we proceed
    scheduler.enqueue_in(timedelta(minutes=1), tasks.discover_engagement_opportunities_from_profile_task,
                         external_id, provider_type, prospect_id)


@receiver(ClientProcessedEngagementAssignmentBatch1.event_signal)
def execute_assignment_batch_1(**kwargs):
  event = kwargs['event']

  # tasks.discover_engagement_opportunities_from_batch_assignments_task.delay(event.batch_id, event.assigned)
