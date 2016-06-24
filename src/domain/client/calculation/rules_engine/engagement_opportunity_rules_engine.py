import logging
from abc import abstractmethod

from src.domain.client.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.domain.common import constants
from src.libs.text_utils.token import token_utils

logger = logging.getLogger(__name__)


class EngagementOpportunityRulesEngine(BaseRulesEngine):
  def __init__(self, eo_id, eo_attrs, rules_data, _token_utils=None):
    if not _token_utils: _token_utils = token_utils
    self._token_utils = _token_utils

    self.eo_id = eo_id
    self.eo_attrs = eo_attrs
    self.rules_data = rules_data

  def score_it(self):
    score, score_attrs = self._apply_score()

    return score, score_attrs

  @abstractmethod
  def _apply_score(self):
    pass


class TwitterEngagementOpportunityRulesEngine(EngagementOpportunityRulesEngine):
  def _apply_score(self):
    score, score_attrs = 0, {}

    tweet_score, tweet_score_attrs = self._apply_tweet_score()
    score += tweet_score
    score_attrs.update(tweet_score_attrs)

    return score, score_attrs

  def _apply_tweet_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    tweet_text = self.eo_attrs.get(constants.TEXT)

    if tweet_text:
      tweet_text_stemmed = self._token_utils.stemmify_snowball_string(tweet_text)

      topic_keywords = self.rules_data.get(constants.TOPIC_KEYWORDS)

      if topic_keywords:

        for k, v in topic_keywords.items():
          tweet_keyword_score = v[constants.RELEVANCE]
          k_stemmed = v[constants.SNOWBALL_STEM]
          if k_stemmed in tweet_text_stemmed:
            score += tweet_keyword_score
            counter[constants.EO_KEYWORD_SCORE] += tweet_keyword_score

        if counter[constants.EO_KEYWORD_SCORE]:
          score_attrs[constants.EO_KEYWORD_SCORE] = counter[constants.EO_KEYWORD_SCORE]

    return score, score_attrs
