import logging

from src.apps.engagement_discovery.providers.twitter.twitter_engagement_discovery_objects import \
  TwitterEngagementOpportunityDiscoveryObject
from src.domain.common import constants
from src.libs.datetime_utils import datetime_parser
from src.libs.python_utils.logging.logging_utils import log_wrapper
from src.libs.social_utils.providers.twitter import twitter_client_service

logger = logging.getLogger(__name__)

_twitter_url_prefix = "https://twitter.com/{0}"


def _is_valid_tweet(tweet):
  ret_val = True

  if ret_val:
    if tweet['in_reply_to_user_id']:
      ret_val = False

  if ret_val:
    if tweet['retweet_count'] >= 20 or tweet['favorite_count'] >= 20:
      ret_val = False

  if ret_val:
    if tweet['user']['statuses_count'] < 50:
      ret_val = False

  if ret_val:
    followers_count = tweet['user']['followers_count']
    following_count = tweet['user']['friends_count']

    if following_count >= 30 and followers_count >= 30:
      # if not true, they're probably not active on twitter, maybe just trying it out and not really engaged yet
      if followers_count > 500:
        ret_val = (following_count / followers_count) >= .65
        # if less than this number, they have a big following and don't follow as many people as who follow them
    else:
      ret_val = False

  return ret_val


def find_tweets_from_keyword(keyword, _twitter_client_service=None, **kwargs):
  ret_val = []
  if not _twitter_client_service:
    _twitter_client_service = twitter_client_service

  search_log_message = (
    "Searching twitter for keyword: %s",
    keyword
  )

  with log_wrapper(logger.debug, *search_log_message):
    tweets_from_keywords = _twitter_client_service.search_twitter_by_keywords(
        keyword,
        include_entities=True,
        exclude_retweets=True,
        **kwargs
    )

  if kwargs.get('screen_name'):
    valid_tweets = tweets_from_keywords

  else:
    valid_tweet_log_message = (
      "Getting valid tweets for keyword: %s",
      keyword
    )

    with log_wrapper(logger.debug, *valid_tweet_log_message):

      tweets_from_keywords = [tweet for tweet in tweets_from_keywords if _is_valid_tweet(tweet)]

      valid_tweets = tweets_from_keywords

  for tweet in valid_tweets:
    username = tweet['user']['screen_name']

    profile_url = _twitter_url_prefix.format(username)
    tweet_id = tweet['id_str']
    url = "{0}/status/{1}".format(profile_url, tweet_id)
    text = tweet['text']
    tweet_created_date = tweet["created_at"]
    tweet_websites = _get_tweet_websites(tweet)

    tweet_data = {
      constants.URL: url, constants.TEXT: text,
    }

    if tweet_websites: tweet_data[constants.WEBSITES] = tweet_websites

    ret_val.append(
        TwitterEngagementOpportunityDiscoveryObject(
            username,
            tweet_id,
            constants.Provider.TWITTER,
            constants.ProviderAction.TWITTER_TWEET,
            tweet,
            tweet_data,
            datetime_parser.get_datetime(tweet_created_date)
        )
    )

  return ret_val


def _get_tweet_websites(tweet):
  tweet_websites = []
  entities = tweet['entities']

  # twitter stores urls in a tweets's field `entities`.
  entity_urls_key = entities.get('urls', [])
  tweet_websites.extend(x['expanded_url'] for x in entity_urls_key)
  return tweet_websites
