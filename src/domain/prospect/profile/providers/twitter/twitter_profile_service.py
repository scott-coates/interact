import logging

from src.domain.common import constants
from src.libs.python_utils.logging.logging_utils import log_wrapper
from src.libs.social_utils.providers.twitter import twitter_search_utils

logger = logging.getLogger(__name__)
_twitter_url_prefix = "https://twitter.com/{0}"


def get_twitter_attrs(provider_external_id):
  return _get_twitter_profile_data(provider_external_id)


def _get_twitter_profile_data(provider_external_id, _search=twitter_search_utils, **kwargs):
  log_message = (
    "Get twitter profile data. twitter_id: %s",
    provider_external_id
  )

  twitter_search_log_message = (
    "Performing twitter search. twitter_id: %s",
    provider_external_id
  )

  with log_wrapper(logger.debug, *log_message):

    with log_wrapper(logger.debug, *twitter_search_log_message):
      user_data = _search.search_twitter_by_user(provider_external_id, **kwargs)

    profile_data = user_data[0]['user']

    profile_url = _twitter_url_prefix.format(provider_external_id)
    name = profile_data['name']
    bio = profile_data['description']
    followers_count = profile_data['followers_count']
    following_count = profile_data['friends_count']
    location = profile_data['location']

    user_websites = _get_twitter_profile_websites(profile_data)

    twitter_profile_data = {
      constants.URL: profile_url, constants.NAME: name,
      constants.Profile.FOLLOWERS_COUNT: followers_count, constants.Profile.FOLLOWING_COUNT: following_count
    }

    if bio: twitter_profile_data[constants.BIO] = bio
    if user_websites: twitter_profile_data[constants.WEBSITES] = user_websites
    if location: twitter_profile_data[constants.LOCATION] = location

  return twitter_profile_data


def _get_twitter_profile_websites(profile_data):
  user_websites = []
  try:
    entities = profile_data['entities']

    # twitter stores urls in a user's profile field `Description`.
    entity_url_key = entities.get('url')
    if entity_url_key:
      urls = entity_url_key.get('urls', [])
      user_websites.extend(x['expanded_url'] for x in urls)

    # twitter ALSO stores urls in a user's profile field `URL`.
    # So a user might store urls in their description field or the pre-defined field for links.
    entity_description_key = entities.get('description')
    if entity_description_key:
      urls = entity_description_key.get('urls', [])
      user_websites.extend(x['expanded_url'] for x in urls)

    # sometimes twitter can return null expanded_urls
    user_websites = [x for x in user_websites if x]
  except KeyError as e:
    logger.debug(e)
  return user_websites