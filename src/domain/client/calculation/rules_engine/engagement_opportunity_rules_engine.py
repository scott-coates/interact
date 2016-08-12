import logging
from abc import abstractmethod

from src.domain.client.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.domain.common import constants
from src.libs.text_utils.token import token_utils

logger = logging.getLogger(__name__)


class EngagementOpportunityRulesEngine(BaseRulesEngine):
  def __init__(self, eo_id, eo_attrs, eo_topic_ids, rules_data, _token_utils=None):
    if not _token_utils: _token_utils = token_utils
    self._token_utils = _token_utils

    self.eo_id = eo_id
    self.eo_attrs = eo_attrs
    self.eo_topic_ids = eo_topic_ids
    self.rules_data = rules_data

  def score_it(self):
    score, score_attrs, counter = self._get_default_score_items()

    topic_score, topic_score_attrs = self._apply_topic_score()
    score += topic_score
    score_attrs.update(topic_score_attrs)

    internal_score, internal_score_attrs = self._apply_score()
    score += internal_score
    score_attrs.update(internal_score_attrs)

    return score, score_attrs

  def _apply_topic_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    topics = self.rules_data.get(constants.TOPICS)

    if topics:

      for k, v in topics.items():
        topic_score = v[constants.RELEVANCE]

        topic_id = v[constants.ID]

        if topic_id in self.eo_topic_ids:
          score += topic_score
          counter[constants.EO_TOPIC_SCORE] += topic_score

          score_attrs[constants.EO_TOPIC_SCORE][constants.SCORE_ATTRS][k] = {
            constants.RELEVANCE: topic_score
          }

          score_attrs[constants.EO_TOPIC_SCORE][constants.SCORE] = counter[constants.EO_TOPIC_SCORE]

    return score, score_attrs

  @abstractmethod
  def _apply_score(self):
    pass


class TwitterEngagementOpportunityRulesEngine(EngagementOpportunityRulesEngine):
  def _apply_score(self):
    score, score_attrs = 0, {}

    mention_score, mention_score_attrs = self._apply_mention_score()
    score += mention_score
    score_attrs.update(mention_score_attrs)

    return score, score_attrs

  def _apply_mention_score(self):
    share_text = ('via @',)

    score, score_attrs, counter = self._get_default_score_items()

    is_retweet = self.eo_attrs.get(constants.IS_RETWEET)

    if not is_retweet:
      text = self.eo_attrs.get(constants.TEXT, '').lower()
      if not any(t for t in share_text if t in text):
        mentions = self.eo_attrs.get(constants.MENTIONS)

        if mentions:
          mention_score = len(mentions)
          score += mention_score
          score_attrs[constants.EO_MENTION_SCORE][constants.SCORE] = mention_score

    return score, score_attrs
