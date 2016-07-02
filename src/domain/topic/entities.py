from src.domain.topic.events import TopicCreated1
from src.domain.topic.service import get_topic_stems
from src.libs.common_domain.aggregate_base import AggregateBase


class Topic(AggregateBase):
  @classmethod
  def from_attrs(cls, id, name):
    ret_val = cls()

    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    stem, collapsed_stem = get_topic_stems(name)

    ret_val._raise_event(TopicCreated1(id, name, stem, collapsed_stem))

    return ret_val

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name

  def __str__(self):
    return 'Topic {id}: {name}'.format(id=self.id, name=self.name)
