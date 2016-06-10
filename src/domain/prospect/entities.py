from src.domain.prospect.events import ProspectCreated1
from src.libs.common_domain.aggregate_base import AggregateBase


class Prospect(AggregateBase):
  def __init__(self):
    super().__init__()
    self._profiles = []

  @classmethod
  def from_attrs(cls, id, attrs):
    ret_val = cls()

    if not id:
      raise TypeError("id is required")

    ret_val._raise_event(ProspectCreated1(id, attrs))

    return ret_val

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.attrs = event.attrs

  def __str__(self):
    return 'Prospect {id}'.format(id=self.id)
