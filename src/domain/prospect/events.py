from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer


class ProspectCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, attrs):
    super().__init__()


class Prospect1AddedProfile(DomainEvent):
  event_func_name = 'profile_added_to_prospect_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, profile_external_id, provider_type, attrs):
    super().__init__()


class ProspectAddedEngagementOpportunityToProfile(DomainEvent):
  event_func_name = 'eo_added_to_profile_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, engagement_opportunity_external_id, engagement_opportunity_attrs, provider_type,
               provider_action_type, created_at, profile_id):
    super().__init__()
