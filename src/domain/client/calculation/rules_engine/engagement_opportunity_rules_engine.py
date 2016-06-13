import logging
from abc import abstractmethod

from src.domain.client.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.libs.python_utils.collections import iter_utils

logger = logging.getLogger(__name__)


class EngagementOpportunityRulesEngine(BaseRulesEngine):
  def __init__(self, engagement_opportunity, calc_data, _iter_utils=None):
    if not _iter_utils: _iter_utils = iter_utils
    self._iter_utils = _iter_utils

    self.engagement_opportunity = engagement_opportunity
    self.calc_data = calc_data

  def score_it(self):
    score, score_attrs = self._apply_score()

    return score, score_attrs

  @abstractmethod
  def _apply_score(self):
    pass


class TwitterEngagementOpportunityRulesEngine(EngagementOpportunityRulesEngine):
  def __init__(self, engagement_opportunity, calc_data, _iter_utils=None, _scraper_utils=None, _text_parser=None):
    # if not _scraper_utils: _scraper_utils = scraper_utils
    # self._scraper_utils = _scraper_utils
    #
    # if not _text_parser: _text_parser = text_parser
    # self._text_parser = _text_parser

    super().__init__(engagement_opportunity, calc_data, _iter_utils)

  def _apply_score(self):
    score, score_attrs = 0, {}

    # tweet_score, tweet_score_attrs = self._apply_tweet_score()
    # score += tweet_score
    # score_attrs.update(tweet_score_attrs)
    #
    # website_score, website_score_attrs = self._apply_tweet_score()
    # score += website_score
    # score_attrs.update(website_score_attrs)

    return score, score_attrs

  def _apply_tweet_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    tweet_text = self.engagement_opportunity.engagement_opportunity_attrs.get(constants.TEXT)

    if tweet_text:

      tweet_text_ta_topic_score = self._tweet_text_ta_topic_score

      client_topics = self.calc_data[constants.STEMMED_TA_TOPIC_KEYWORDS]

      tweet_text = self._iter_utils.stemmify_string(tweet_text)

      for stemmed_topic_keyword in client_topics:
        if stemmed_topic_keyword in tweet_text:
          score += tweet_text_ta_topic_score
          counter[constants.TWEET_TEXT_TA_TOPIC_KEYWORD_SCORE] += tweet_text_ta_topic_score
          # give, at most, 1 point per topic mention
          break

      if counter[constants.TWEET_TEXT_TA_TOPIC_KEYWORD_SCORE]:
        x = constants.TWEET_TEXT_TA_TOPIC_KEYWORD_SCORE

        score_attrs[x] = counter[x]

    return score, score_attrs

  def _apply_website_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    websites = self.engagement_opportunity.engagement_opportunity_attrs.get(constants.WEBSITES)

    if websites:

      website_text_ta_topic_score = self._website_text_ta_topic_score

      client_topics = self.calc_data[constants.STEMMED_TA_TOPIC_KEYWORDS]

      for website in websites:
        try:
          content = self._scraper_utils.get_main_content_from_web_page(website[constants.URL])
          content = self._text_parser.strip_html(content)
          content = self._iter_utils.stemmify_string(content)
          for stemmed_keyword in client_topics:
            if stemmed_keyword in content:
              score += website_text_ta_topic_score
              counter[constants.EO_WEBSITE_TA_TOPIC_KEYWORD_SCORE] += website_text_ta_topic_score
        except Exception:
          logger.debug("Error summarizing websites", exc_info=True)
          continue

      if counter[constants.EO_WEBSITE_TA_TOPIC_KEYWORD_SCORE]:
        x = constants.EO_WEBSITE_TA_TOPIC_KEYWORD_SCORE

        score_attrs[x] = counter[x]

    return score, score_attrs

  @property
  def _tweet_text_ta_topic_score(self):
    return 1

  @property
  def _website_text_ta_topic_score(self):
    return 1
