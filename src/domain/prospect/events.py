from django.dispatch import Signal

from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer

duplicate_profile_discovered = Signal(providing_args=['duplicate_prospect_id', 'existing_external_id',
                                                      'existing_provider_type'])


class ProspectCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, attrs):
    super().__init__()


class ProspectMarkedAsDuplicate(DomainEvent):
  event_func_name = 'marked_as_duplicate_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, existing_prospect_id):
    super().__init__()


class ProspectDeleted(DomainEvent):
  event_func_name = 'deleted_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, reason):
    super().__init__()


class ProspectAddedProfile1(DomainEvent):
  event_func_name = 'profile_added_to_prospect_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, external_id, provider_type, attrs, prospect_is_duplicated, existing_prospect_id):
    super().__init__()


class ProspectUpdatedAttrsFromProfile1(DomainEvent):
  event_func_name = 'attrs_updated_from_profile_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, attrs, profile_id):
    super().__init__()


class EngagementOpportunityAddedToProfile1(DomainEvent):
  event_func_name = 'eo_added_to_profile_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, external_id, attrs, provider_type,
               provider_action_type, created_date, prospect_is_duplicated, existing_prospect_id, profile_id):
    super().__init__()


class TopicAddedToEngagementOpportunity1(DomainEvent):
  event_func_name = 'topic_added_to_eo_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, engagement_opportunity_id, topic_id):
    super().__init__()
