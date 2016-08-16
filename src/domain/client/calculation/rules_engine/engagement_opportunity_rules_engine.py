import logging
from abc import abstractmethod
from itertools import chain

from nltk.metrics.distance import jaccard_distance

from src.domain.client.calculation.processing.data_processor import get_comparative_text_from_tweet
from src.domain.client.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.domain.common import constants
from src.libs.text_utils.token import token_utils

logger = logging.getLogger(__name__)


class EngagementOpportunityRulesEngine(BaseRulesEngine):
  def __init__(self, eo_id, eo_attrs, eo_topic_ids, prospect_id, rules_data, _token_utils=None):
    super().__init__()

    if not _token_utils: _token_utils = token_utils
    self._token_utils = _token_utils

    self.eo_id = eo_id
    self.eo_attrs = eo_attrs
    self.eo_topic_ids = eo_topic_ids
    self.prospect_id = prospect_id
    self.rules_data = rules_data

  def get_score_attrs(self):
    score_attrs, counter = self._get_default_score_attr_items()

    topic_score_attrs = self._get_topic_score_attrs()
    score_attrs.update(topic_score_attrs)

    internal_score_attrs = self._get_score_attrs()
    score_attrs.update(internal_score_attrs)

    return score_attrs

  def _get_topic_score_attrs(self):
    score_attrs, counter = self._get_default_score_attr_items()

    topics = self.rules_data.get(constants.TOPICS)

    if topics:

      for k, v in topics.items():

        topic_id = v[constants.ID]

        if topic_id in self.eo_topic_ids:
          counter[constants.EO_TOPIC] += v[constants.RELEVANCE]

          score_attrs[constants.EO_TOPIC][constants.SCORE_ATTRS][topic_id] = {
            constants.NAME: k
          }

          # score_attrs[constants.EO_TOPIC][constants.SCORE_ATTRS][k] = {
          #   constants.RELEVANCE: topic_score
          # }
          # todo move over

          # todo provide easier way other than writing out
          # --- score_attrs[constants.EO_TOPIC][constants.SCORE_ATTRS][constants.COUNT][constants.DATA] ---
          # i missed one dimension and threw the whole thing off in the calc phase cause I had:
          # score_attrs[constants.EO_TOPIC][constants.COUNT][constants.DATA]
          score_attrs[constants.EO_TOPIC][constants.COUNT][constants.DATA] = counter[constants.EO_TOPIC]

    return score_attrs

  @abstractmethod
  def _get_score_attrs(self):
    pass


class TwitterEngagementOpportunityRulesEngine(EngagementOpportunityRulesEngine):
  def _get_score_attrs(self):
    score_attrs = {}

    engagement_score_attrs = self._get_engagement_score_attrs()
    score_attrs.update(engagement_score_attrs)

    spam_score_attrs = self._get_spam_score_attrs()
    score_attrs.update(spam_score_attrs)

    return score_attrs

  def _get_engagement_score_attrs(self):
    share_text = ('via @',)

    score_attrs, counter = self._get_default_score_attr_items()

    is_retweet = self.eo_attrs.get(constants.IS_RETWEET)

    if not is_retweet:
      text = self.eo_attrs[constants.TEXT].lower()
      if not any(t for t in share_text if t in text):
        mentions = self.eo_attrs.get(constants.MENTIONS)

        if mentions:
          score_attrs[constants.EO_ENGAGEMENT][constants.COUNT][constants.DATA] = self.DEFAULT_COUNT_VALUE

    return score_attrs

  def _get_spam_score_attrs(self):
    score_attrs, counter = self._get_default_score_attr_items()

    text = self.eo_attrs[constants.TEXT]

    comparative_text = get_comparative_text_from_tweet(text)

    recent_eos = self.rules_data.get(constants.RECENT_EOS)

    if recent_eos:

      for recent_eo in recent_eos:

        if self.eo_id != recent_eo[constants.ID] and self.eo_id not in recent_eo[constants.SIMILAR_EOS]:
          recent_comparative_text = recent_eo[constants.COMPARATIVE_TEXT]

          distance = jaccard_distance(set(comparative_text), set(recent_comparative_text))

          if distance < .5:
            recent_eo[constants.SIMILAR_EOS].append(self.eo_id)

      similar_eo_count = list(chain.from_iterable(r[constants.SIMILAR_EOS] for r in recent_eos))
      if similar_eo_count:
        score_attrs[constants.EO_SPAM][constants.COUNT][constants.DATA] = self.DEFAULT_COUNT_VALUE

    return score_attrs
