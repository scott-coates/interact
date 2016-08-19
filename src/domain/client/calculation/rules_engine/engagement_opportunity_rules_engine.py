import logging
from abc import abstractmethod

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
    score_attrs = {}

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
          # should the rules engine be concerned with relevance? or should the calculator care?
          # I started going down the route of moving over this logic to the calculator because I didn't think rules
          # engine should care about influencing final score. However, I ran into problems right away with counting
          # ints vs lists. We'd have to have logic to look for this key or a type `list`. Then I realized that client
          #  preferences already seem to influence rules engines (consider location scores, or in the future,
          # persons vs companies, etc. Also, what if we did successfully move this logic over the calculator,
          # how would the calc factor in relevance? Once the calc computes a score based on integer counts,
          # we'd still need to factor in topic_id relevance? But the score has already been calculated, so now what?
          # So we probably wouldn't change the score after the fact, we'd probably bump up the counts at the very
          # beginning, changing the input, which is essentially doing the same thing we'd be doing here, only making
          # it way more convoluted.
          relevance = v[constants.RELEVANCE]
          counter[constants.EO_TOPIC] += relevance

          self._set_score_attrs_meta(score_attrs, constants.EO_TOPIC, topic_id, {
            constants.NAME: k,
            constants.RELEVANCE: relevance
          })

    self._set_score_attrs_counter_value(score_attrs, constants.EO_TOPIC, counter)

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
          counter[constants.EO_ENGAGEMENT] += self.DEFAULT_COUNT_VALUE

    self._set_score_attrs_counter_value(score_attrs, constants.EO_ENGAGEMENT, counter)
    return score_attrs

  def _get_spam_score_attrs(self):
    score_attrs, counter = self._get_default_score_attr_items()

    text = self.eo_attrs[constants.TEXT]

    comparative_text = get_comparative_text_from_tweet(text)
    if comparative_text:

      recent_eos = self.rules_data.get(constants.RECENT_EOS)

      if recent_eos:

        for recent_eo in recent_eos:

          if self.eo_id != recent_eo[constants.ID] and self.eo_id not in recent_eo[constants.SIMILAR_EOS]:

            recent_comparative_text = recent_eo[constants.COMPARATIVE_TEXT]

            if recent_comparative_text:
              distance = jaccard_distance(set(comparative_text), set(recent_comparative_text))

              if distance < .5:
                recent_eo[constants.SIMILAR_EOS].append(self.eo_id)

        similar_eo_ids = [r[constants.ID] for r in recent_eos if self.eo_id in r[constants.SIMILAR_EOS]]
        if similar_eo_ids:
          self._set_score_attrs_meta(score_attrs, constants.EO_SPAM, constants.DATA, similar_eo_ids)

          counter[constants.EO_SPAM] += self.DEFAULT_COUNT_VALUE

    self._set_score_attrs_counter_value(score_attrs, constants.EO_SPAM, counter)
    return score_attrs
