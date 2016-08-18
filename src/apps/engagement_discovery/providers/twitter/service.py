import logging

from src.apps.engagement_discovery.engagement_discovery_objects import EngagementOpportunityDiscoveryObject
from src.apps.engagement_discovery.providers.twitter.twitter_engagement_discovery_objects import \
  TwitterEngagementOpportunityDiscoveryObject
from src.apps.engagement_discovery.signals import engagement_opportunity_discovered
from src.apps.social.providers.twitter import twitter_service
from src.domain.common import constants
from src.libs.datetime_utils import datetime_parser
from src.libs.python_utils.logging.logging_utils import log_wrapper
from src.libs.web_utils.url.url_utils import get_unique_urls_from_iterable

logger = logging.getLogger(__name__)
_twitter_url_prefix = "https://twitter.com/{0}"


def discover_engagement_opportunities_from_twitter_ta_topic_option(ta_topic_option):
  log_message = ('Discovery for ta topic option %s', ta_topic_option)

  kwargs = {}

  with log_wrapper(logger.debug, *log_message):

    # if we want to get additional parameters (like geocode, since, follower count)
    geocode = ta_topic_option.option_attrs.get('geocode')
    if geocode:
      kwargs['geocode'] = geocode

    since = ta_topic_option.option_attrs.get('since', 'q')
    kwargs['since'] = since

    kwargs['count'] = 1  # todo remove me

    twitter_eos = _find_tweets_from_keyword(ta_topic_option.option_name, **kwargs)

    total_eos_count = len(twitter_eos)
    counter = 1

    logger.debug("EO's to create for ta topic option %s %i", ta_topic_option, total_eos_count)

    for twitter_eo in twitter_eos:
      _send_eo_discovery(twitter_eo, counter, total_eos_count)
      counter += 1


def discover_engagement_opportunities_from_twitter_user(screen_name):
  log_message = ('Discovery for user %s', screen_name)

  with log_wrapper(logger.debug, *log_message):
    twitter_eos = _find_tweets_from_user(screen_name)

    total_eos_count = len(twitter_eos)
    counter = 1

    logger.debug("EO's to create for user %s %i", screen_name, total_eos_count)

    for twitter_eo in twitter_eos:
      _send_eo_discovery(twitter_eo, counter, total_eos_count)
      counter += 1


def _send_eo_discovery(twitter_eo, counter, total_eos_count):
  discovery_object = EngagementOpportunityDiscoveryObject(
      twitter_eo.screen_name,
      twitter_eo.twitter_obj['id_str'],
      twitter_eo.twitter_obj_attrs,
      twitter_eo.created_date,
      twitter_eo.provider_type,
      twitter_eo.provider_action_type
  )

  logger.debug('Sending discovery object %i out of %i. Username: %s. Tweet: %s', counter, total_eos_count,
               twitter_eo.screen_name,
               twitter_eo.twitter_obj['text'])

  engagement_opportunity_discovered.send(
      EngagementOpportunityDiscoveryObject,
      engagement_opportunity_discovery_object=discovery_object)


def _find_tweets_from_keyword(keyword, _twitter_service=None, **kwargs):
  if not _twitter_service:    _twitter_service = twitter_service

  search_log_message = ("Searching twitter for keyword: %s", keyword)

  with log_wrapper(logger.debug, *search_log_message):
    tweets_from_keywords = _twitter_service.search_twitter_by_keywords(
        keyword,
        include_entities=True,
        exclude_retweets=True,
        exclude_replies=True,
        **kwargs
    )

  ret_val = _create_tweet_eo_object(tweets_from_keywords)

  return ret_val


def _find_tweets_from_user(screen_name, _twitter_service=None):
  if not _twitter_service:    _twitter_service = twitter_service

  search_log_message = ("Searching user timeline: %s", screen_name)

  with log_wrapper(logger.debug, *search_log_message):
    tweets_from_user = _twitter_service.search_twitter_by_user(screen_name, since='y', count=1)

  ret_val = _create_tweet_eo_object(tweets_from_user)

  return ret_val


def _create_tweet_eo_object(tweets):
  ret_val = []

  for tweet in tweets:
    screen_name = tweet['user'][constants.SCREEN_NAME]

    profile_url = _twitter_url_prefix.format(screen_name)
    tweet_id = tweet['id_str']
    url = "{0}/status/{1}".format(profile_url, tweet_id)
    text = tweet[constants.TEXT]
    is_retweet = _is_retweet(tweet, text)
    tweet_created_date = tweet["created_at"]
    tweet_websites = _get_tweet_websites(tweet)
    tweet_mentions = _get_tweet_mentions(tweet)

    tweet_data = {
      constants.URL: url, constants.TEXT: text,
      constants.IS_RETWEET: is_retweet,
    }

    if tweet_websites: tweet_data[constants.WEBSITES] = tweet_websites
    if tweet_mentions: tweet_data[constants.MENTIONS] = tweet_mentions

    ret_val.append(
        TwitterEngagementOpportunityDiscoveryObject(
            screen_name,
            tweet_id,
            constants.Provider.TWITTER,
            constants.ProviderAction.TWITTER_TWEET,
            tweet,
            tweet_data,
            datetime_parser.get_datetime(tweet_created_date)
        )
    )

  return ret_val


def _is_retweet(tweet, text):
  ret_val = False

  # http://stackoverflow.com/questions/18869688/twitter-api-check-if-a-tweet-is-a-retweet
  if 'retweeted_status' in tweet:
    ret_val = True
  else:
    if text.startswith('RT '):
      ret_val = True

  return ret_val


def _get_tweet_websites(tweet):
  tweet_websites = []
  entities = tweet['entities']

  # twitter stores urls in a tweets's field `entities`.
  entity_urls_key = entities.get('urls', [])
  tweet_websites.extend(x['expanded_url'] for x in entity_urls_key)
  tweet_websites = get_unique_urls_from_iterable(tweet_websites)

  return tweet_websites


def _get_tweet_mentions(tweet):
  tweet_mentions = []
  entities = tweet['entities']

  # twitter stores mentions in a tweets's field `entities`.
  entity_mentions_key = entities.get('user_mentions', [])
  tweet_mentions.extend(_get_user_mention(x) for x in entity_mentions_key)

  return tweet_mentions


def _get_user_mention(mention):
  ret_val = {
    constants.ID: mention['id_str'],
    constants.NAME: mention[constants.NAME],
    constants.EXTERNAL_ID: mention[constants.SCREEN_NAME]
  }

  return ret_val
