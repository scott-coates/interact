from src.domain.topic.events import TopicCreated1
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.text_utils.token import token_utils


class Topic(AggregateBase):
  @classmethod
  def from_attrs(cls, id, name, _token_utils=None):
    if not _token_utils: _token_utils = token_utils
    ret_val = cls()

    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    stem = _token_utils.stemmify_string(name)
    ret_val._raise_event(TopicCreated1(id, name, stem))

    return ret_val

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.stem = event.stem

  def __str__(self):
    return 'Topic {id}: {name}'.format(id=self.id, name=self.name)
