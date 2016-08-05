from outliers import smirnov_grubbs as grubbs

from src.apps.geo import service as geo_service
from src.domain.client.calculation import calculator, score_processor
from src.domain.client.events import ClientCreated1, ClientAssociatedWithTopic1, \
  ClientAddedTargetAudienceTopicOption1, \
  ClientProcessedEngagementAssignmentBatch1
from src.domain.common import constants
from src.libs.common_domain.aggregate_base import AggregateBase


class Client(AggregateBase):
  def __init__(self):
    super().__init__()
    self._ta_topics = []
    self._eas = []

  @classmethod
  def from_attrs(cls, id, name, ta_attrs, _geo_service=None):
    if not _geo_service: _geo_service = geo_service

    ret_val = cls()

    if not id:
      raise TypeError("id is required")

    if not name:
      raise TypeError("name is required")

    if ta_attrs is None:
      raise TypeError("ta_attrs is required")

    if not isinstance(ta_attrs, dict):
      raise TypeError("ta_attrs must be a dict")

    for v in ta_attrs.values():
      if not isinstance(v, (list, tuple)):
        raise TypeError("Each value must be an iterable")

    locations = ta_attrs.get(constants.LOCATIONS)

    if locations:
      locations = [_geo_service.get_geocoded_address_dict(l) for l in locations]
      ta_attrs[constants.LOCATIONS] = locations

    ret_val._raise_event(ClientCreated1(id, name, ta_attrs))

    return ret_val

  def associate_with_topic(self, id, relevance, topic_id):
    self._raise_event(ClientAssociatedWithTopic1(id, relevance, topic_id))

  def add_topic_option(self, id, name, type, attrs, ta_topic_id):
    ta_topic = self._get_ta_topic_by_id(ta_topic_id)

    self._raise_event(
        ClientAddedTargetAudienceTopicOption1(id, name, type, attrs, ta_topic_id, ta_topic.relevance, ta_topic.topic_id)
    )

  def add_ea_batch(self, batch_id, batch_eas, _score_processor=None, _outlier_utils=None):
    if not _score_processor: _score_processor = score_processor
    if not _outlier_utils: _outlier_utils = grubbs

    if not batch_id:
      raise TypeError("batch_id is required")

    self._check_eas(batch_eas)

    for b in batch_eas:
      b[constants.SCORE] = _score_processor.process_score(b[constants.SCORE_ATTRS])

    scores = sorted([b[constants.SCORE] for b in batch_eas])
    accepted = _outlier_utils.test(scores, 0.01)
    min_score, max_score = min(accepted), max(accepted)

    assigned = []
    skipped = []

    for b in batch_eas:
      assigned.append(b)
      # if min_score <= b[constants.SCORE] <= max_score:
      # else:
      #   skipped.append(b)

    self._raise_event(
        ClientProcessedEngagementAssignmentBatch1(batch_id, assigned, skipped, scores, min_score, max_score)
    )

  def get_engagement_assignment_score_attrs(self, assignment_attrs, _calculator=None):
    if not _calculator: _calculator = calculator

    score_attrs = _calculator.get_engagement_assignment_score_attrs(self.id, assignment_attrs)

    return score_attrs

  def _check_eas(self, batch_eas):

    for b in batch_eas:

      if not b[constants.ID]:
        raise TypeError("id is required")

      if not b[constants.PROSPECT_ID]:
        raise TypeError("prospect_id is required")

      self._check_attrs(b[constants.ATTRS])
      self._check_attrs(b[constants.SCORE_ATTRS])

  def _check_attrs(self, attr):
    if not isinstance(attr, dict):
      raise TypeError("attrs must be a dict")

    for v in attr.values():
      if not isinstance(v, (list, tuple, dict)):
        raise TypeError("Each value must be an iterable")

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.name = event.name
    self.ta_attrs = event.ta_attrs

  def _handle_associated_with_topic_1_event(self, event):
    self._ta_topics.append(TargetAudienceTopic(event.id, event.relevance, event.topic_id))

  def _handle_added_target_audience_topic_option_1_event(self, event):
    ta_topic = self._get_ta_topic_by_id(event.ta_topic_id)
    ta_topic._add_topic_option(**event.data)

  def _handle_processed_ea_batch_1_event(self, event):
    for ea in event.assigned:
      self._eas.append(
          EngagementAssignment(**ea)
      )

  def _get_ta_topic_by_id(self, ta_topic_id):
    ta_topic = next(t for t in self._ta_topics if t.id == ta_topic_id)
    return ta_topic

  def __str__(self):
    return 'Client {id}: {name}'.format(id=self.id, name=self.name)


class TargetAudienceTopic:
  def __init__(self, id, relevance, topic_id):
    self._ta_topic_options = []

    if not id:
      raise TypeError("id is required")

    if relevance is None:
      raise TypeError("relevance is required")

    if not topic_id:
      raise TypeError("topic_id is required")

    self.id = id
    self.relevance = relevance
    self.topic_id = topic_id

  # noinspection PyUnusedLocal
  def _add_topic_option(self, id, name, type, attrs, ta_topic_id, **kwargs):
    option = TargetAudienceTopicOption(id, name, type, attrs, ta_topic_id)
    self._ta_topic_options.append(option)

  def __str__(self):
    return 'TATopic {id}'.format(id=self.id)


class TargetAudienceTopicOption:
  def __init__(self, id, name, type, attrs, ta_topic_id):
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

    self.id = id
    self.name = name
    self.type = type
    self.attrs = attrs
    self.ta_topic_id = ta_topic_id

  def __str__(self):
    return 'TATopicOption {id}: {name}'.format(id=self.id, name=self.name)


class EngagementAssignment:
  def __init__(self, id, attrs, score, score_attrs, prospect_id):
    if not id:
      raise TypeError("id is required")

    if not attrs:
      raise TypeError("attrs is required")

    if score is None:
      raise TypeError("score is required")

    if score_attrs is None:
      raise TypeError("score_attrs is required")

    if not prospect_id:
      raise TypeError("prospect_id is required")

    self.id = id
    self.attrs = attrs
    self.score = score
    self.score_attrs = score_attrs

    self.prospect_id = prospect_id

  def __str__(self):
    return 'EA {id}: {score}'.format(id=self.id, score=self.score)
