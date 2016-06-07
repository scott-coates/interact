from src.libs.common_domain.domain_event import DomainEvent
from src.libs.common_domain.event_signal import EventSignal
from src.libs.python_utils.objects.object_utils import initializer


class ClientCreated1(DomainEvent):
  event_func_name = 'created_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, id, name, system_created_date):
    super().__init__()


class AssociatedWithTopic1(DomainEvent):
  event_func_name = 'associated_with_topic_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, ta_topic_id, topic_id, system_created_date):
    super().__init__()


class AddedTopicOption1(DomainEvent):
  event_func_name = 'added_topic_option_1'
  event_signal = EventSignal()

  @initializer
  def __init__(self, ta_topic_option_id, name, type, attrs, ta_topic_id, topic_id, system_created_date):
    super().__init__()
