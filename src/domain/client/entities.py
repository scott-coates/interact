from src.domain.client.events import ClientCreated1
from src.libs.common_domain.aggregate_base import AggregateBase


class Client(AggregateBase):
  @classmethod
  def from_attrs(cls, id, name, system_created_date):
    ret_val = cls()

    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    ret_val._raise_event(ClientCreated1(id, name, system_created_date))

    return ret_val

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.system_created_date = event.system_created_date

  def __str__(self):
    return 'Client {id}: {name}'.format(id=self.id, name=self.name)


class TargetAudienceTopic:
  def __init__(self, id, active, topic_id, client_id, system_created_date):

    if not id:
      raise TypeError("id is required")

    if not active:
      raise TypeError("active is required")

    if not topic_id:
      raise TypeError("topic_id is required")

    if not client_id:
      raise TypeError("client_id is required")

    self.id = id
    self.active = active
    self.topic_id = topic_id
    self.client_id = client_id
    self.system_created_date = system_created_date

  def __str__(self):
    return 'TATopic {id}'.format(id=self.id)


class TargetAudienceTopicOption:
  def __init__(self, id, option_name, option_type, attrs, ta_topic_id, system_created_date):

    if not id:
      raise TypeError("id is required")

    if not option_name:
      raise TypeError("option_name is required")

    if not option_type:
      raise TypeError("option_type is required")

    if not attrs:
      raise TypeError("attrs is required")

    if not ta_topic_id:
      raise TypeError("ta_topic_id is required")

    self.id = id
    self.option_name = option_name
    self.option_type = option_type
    self.attrs = attrs
    self.ta_topic_id = ta_topic_id
    self.system_created_date = system_created_date

  def __str__(self):
    return 'TATopicOption {id}'.format(id=self.id)
