from src.domain.topic.events import TopicCreated1
from src.libs.common_domain.aggregate_base import AggregateBase


class Topic(AggregateBase):
  @classmethod
  def from_attrs(cls, id, name, system_created_date):
    ret_val = cls()

    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    ret_val._raise_event(TopicCreated1(id, name, system_created_date))

    return ret_val

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.system_created_date = event.system_created_date

  def __str__(self):
    return 'Topic {id}: {name}'.format(id=self.id, name=self.name)
