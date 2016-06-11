from src.domain.engagement_assignment.events import EngagementAssignmentCreated1
from src.libs.common_domain.aggregate_base import AggregateBase


class EngagementAssignment(AggregateBase):
  @classmethod
  def from_attrs(cls, id, attrs, client_id):
    ret_val = cls()

    if not id:
      raise TypeError("id is required")

    if not attrs:
      raise TypeError("attrs is required")

    if not client_id:
      raise TypeError("client_id is required")

    score = 0
    score_attrs = None

    ret_val._raise_event(EngagementAssignmentCreated1(id, attrs, score, score_attrs, client_id))

    return ret_val

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.attrs = event.attrs
    self.score = event.score
    self.score_attrs = event.score_attrs
    self.client_id = event.client_id

  def __str__(self):
    return 'EA {id}: {score}'.format(id=self.id, score=self.score)
