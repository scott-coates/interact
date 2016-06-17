import logging

from src.apps.engagement_discovery.providers.twitter.twitter_engagement_discovery_objects import \
  TwitterEngagementOpportunityDiscoveryObject
from src.domain.common import constants
from src.libs.datetime_utils import datetime_parser
from src.libs.python_utils.logging.logging_utils import log_wrapper
from src.libs.social_utils.providers.twitter import twitter_client_service

logger = logging.getLogger(__name__)

_twitter_url_prefix = "https://twitter.com/{0}"


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
        exclude_replies=True,
        **kwargs
    )

  for tweet in tweets_from_keywords:
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
