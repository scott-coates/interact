from src.domain.client.events import ClientCreated1, AssociatedWithTopic1, AddedTargetAudienceTopicOption1
from src.libs.common_domain.aggregate_base import AggregateBase


class Client(AggregateBase):
  def __init__(self):
    super().__init__()
    self._ta_topics = []

  @classmethod
  def from_attrs(cls, id, name):
    ret_val = cls()

    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    ret_val._raise_event(ClientCreated1(id, name))

    return ret_val

  def associate_with_topic(self, id, topic_id):
    if not id:
      raise TypeError("id is required")

    if not topic_id:
      raise TypeError("topic_id is required")

    self._raise_event(AssociatedWithTopic1(id, topic_id))

  def add_topic_option(self, id, name, type, attrs, ta_topic_id):
    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    if not type:
      raise TypeError("type is required")

    if not attrs:
      raise TypeError("attrs is required")

    if not ta_topic_id:
      raise TypeError("ta_topic_id is required")

    ta_topic = self._get_ta_topic_by_id(ta_topic_id)

    self._raise_event(
        AddedTargetAudienceTopicOption1(id, name, type, attrs, ta_topic_id, ta_topic.topic_id)
    )

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name

  def _handle_associated_with_topic_1_event(self, event):
    self._ta_topics.append(TargetAudienceTopic(event.id, event.topic_id))

  def _handle_added_target_audience_topic_option_1_event(self, event):
    ta_topic = self._get_ta_topic_by_id(event.ta_topic_id)
    ta_topic._add_topic_option(**event.data)

  def _get_ta_topic_by_id(self, ta_topic_id):
    ta_topic = next(t for t in self._ta_topics if t.id == ta_topic_id)
    return ta_topic

  def __str__(self):
    return 'Client {id}: {name}'.format(id=self.id, name=self.name)


class TargetAudienceTopic:
  def __init__(self, id, topic_id):
    self._ta_topic_options = []

    if not id:
      raise TypeError("id is required")

    if not topic_id:
      raise TypeError("topic_id is required")

    self.id = id
    self.topic_id = topic_id

  # noinspection PyUnusedLocal
  def _add_topic_option(self, id, name, type, attrs, ta_topic_id, **kwargs):
    option = TargetAudienceTopicOption(id, name, type, attrs, ta_topic_id)
    self._ta_topic_options.append(option)

  def __str__(self):
    return 'TATopic {id}'.format(id=self.id)


class TargetAudienceTopicOption:
  def __init__(self, id, name, type, attrs, ta_topic_id):
    self.id = id
    self.name = name
    self.type = type
    self.attrs = attrs
    self.ta_topic_id = ta_topic_id

  def __str__(self):
    return 'TATopicOption {id}: {name}'.format(id=self.id, name=self.name)
