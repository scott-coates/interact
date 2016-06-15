import logging
from abc import abstractmethod

from src.domain.client.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.libs.python_utils.collections import iter_utils

logger = logging.getLogger(__name__)


class ProfileRulesEngine(BaseRulesEngine):
  def __init__(self, profile_id, profile_attrs, rules_data, _iter_utils=None):
    if not _iter_utils: _iter_utils = iter_utils
    self._iter_utils = _iter_utils

    self.profile_id = profile_id
    self.profile_attrs = profile_attrs

    self.rules_data = rules_data

  def score_it(self):
    score, score_attrs = self._apply_score()

    return score, score_attrs

  @abstractmethod
  def _apply_score(self):
    pass


class TwitterProfileRulesEngine(ProfileRulesEngine):
  def _apply_score(self):
    score, score_attrs = 0, {}
    #
    # recent_tweet_score, recent_tweet_score_attrs = self._apply_recent_tweets_score()
    # score += recent_tweet_score
    # score_attrs.update(recent_tweet_score_attrs)
    #
    # followers_score, followers_score_attrs = self._apply_followers_score()
    # score += followers_score
    # score_attrs.update(followers_score_attrs)

    return score, score_attrs

  def _apply_recent_tweets_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    recent_tweets = self.profile.profile_attrs.get(constants.RECENT_TWEETS)

    if recent_tweets:

      client_topics = self.rules_data[constants.STEMMED_TA_TOPIC_KEYWORDS]

      recent_tweets_score = self._recent_tweets_score

      recent_tweets = self._iter_utils.stemmify_iterable(recent_tweets)

      for stemmed_topic_keyword in client_topics:
        for tweet in recent_tweets:
          if stemmed_topic_keyword in tweet:
            score += recent_tweets_score
            counter[constants.RECENT_TWEET_TA_TOPIC_KEYWORD_SCORE] += recent_tweets_score
            # give, at most, 1 point per topic mention
            break

      if counter[constants.RECENT_TWEET_TA_TOPIC_KEYWORD_SCORE]:
        x = constants.RECENT_TWEET_TA_TOPIC_KEYWORD_SCORE

        score_attrs[x] = counter[x]

    return score, score_attrs

  def _apply_followers_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    followers_min, followers_max = self._followers_following_range

    if followers_min and followers_max:

      followers_count = self.profile.profile_attrs.get(constants.FOLLOWERS_COUNT)

      if followers_count:
        follower_ratio_score = self._follower_ratio_score

        if followers_min <= followers_count <= followers_max:
          score += follower_ratio_score
          score_attrs[constants.FOLLOWERS_COUNT_SCORE] = follower_ratio_score

    return score, score_attrs

  @property
  def _recent_tweets_score(self):
    return 1

  @property
  def _followers_following_range(self):
    return (None, None)

  @property
  def _follower_ratio_score(self):
    return 1
