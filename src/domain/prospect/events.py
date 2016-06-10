from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer


class ProspectCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, attrs):
    super().__init__()


class ProfileAddedToProspect1(DomainEvent):
  event_func_name = 'profile_added_to_prospect_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, provider_external_id, provider_type, attrs):
    super().__init__()
