import logging

from src.apps.engagement_discovery.engagement_discovery_objects import EngagementOpportunityDiscoveryObject
from src.apps.engagement_discovery.providers.twitter.twitter_engagement_discovery_objects import \
  TwitterEngagementOpportunityDiscoveryObject
from src.apps.engagement_discovery.signals import engagement_opportunity_discovered
from src.domain.common import constants
from src.libs.datetime_utils import datetime_parser
from src.libs.python_utils.logging.logging_utils import log_wrapper
from src.libs.social_utils.providers.twitter import twitter_client_service
from src.libs.web_utils.url.url_utils import get_unique_urls_from_iterable

logger = logging.getLogger(__name__)
_twitter_url_prefix = "https://twitter.com/{0}"


def discover_engagement_opportunities_from_twitter_ta_topic_option(ta_topic_option, **kwargs):
  log_message = ('Discovery for ta topic option %s. kwargs: %s', ta_topic_option, kwargs)

  with log_wrapper(logger.debug, *log_message):

    # if we want to get additional parameters (like geocode, since, follower count)
    geocode = ta_topic_option.option_attrs.get('geocode')
    if geocode:
      kwargs['geocode'] = geocode

    since = ta_topic_option.option_attrs.get('since', 'q')
    kwargs['since'] = since

    kwargs['count'] = 1

    twitter_eos = _find_tweets_from_keyword(ta_topic_option.option_name, **kwargs)

    total_eos_count = len(twitter_eos)
    counter = 1

    logger.debug("EO's to create for ta topic option %s %i", ta_topic_option, total_eos_count)

    for twitter_eo in twitter_eos:
      discovery_object = EngagementOpportunityDiscoveryObject(
          twitter_eo.username,
          twitter_eo.twitter_obj['id_str'],
          twitter_eo.twitter_obj_attrs,
          twitter_eo.created_date,
          twitter_eo.provider_type,
          twitter_eo.provider_action_type
      )

      logger.debug('Sending discovery object %i out of %i. Username: %s. Tweet: %s', counter, total_eos_count,
                   twitter_eo.username,
                   twitter_eo.twitter_obj['text'])

      engagement_opportunity_discovered.send(
          EngagementOpportunityDiscoveryObject,
          engagement_opportunity_discovery_object=discovery_object)

      counter += 1


def _find_tweets_from_keyword(keyword, _twitter_client_service=None, **kwargs):
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
  tweet_websites = get_unique_urls_from_iterable(tweet_websites)

  return tweet_websites
