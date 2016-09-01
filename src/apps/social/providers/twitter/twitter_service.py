from src.apps.key_value.common import get_app_name
from src.libs.key_value_utils.service import record_rate_limit, get_rate_limit_count
from src.libs.social_utils.providers.twitter import twitter_search_utils, twitter_client_service


def search_twitter_by_user(screen_name, _search=twitter_search_utils, **kwargs):
  search_name = 'user_timeline'
  _check_rate_limit(search_name, 300)
  ret_val = _search.search_twitter_by_user(screen_name, **kwargs)
  _record_twitter_api_call(search_name)
  return ret_val


def get_user_info(screen_name, _search=twitter_search_utils, **kwargs):
  search_name = 'user_profile'
  _check_rate_limit(search_name, 180)
  ret_val = _search.get_user_info(screen_name, **kwargs)
  _record_twitter_api_call(search_name)
  return ret_val


def search_twitter_by_keywords(keyword, _twitter_client_service=twitter_client_service, **kwargs):
  search_name = 'search_tweets'
  _check_rate_limit(search_name, 450)
  ret_val = _twitter_client_service.search_twitter_by_keywords(keyword, **kwargs)
  _record_twitter_api_call(search_name)
  return ret_val


def _record_twitter_api_call(search_name):
  record_rate_limit(get_app_name('twitter_api_call:{0}', search_name), 15 * 60)


def _check_rate_limit(search_name, limit):
  count = get_rate_limit_count(get_app_name('twitter_api_call:{0}', search_name))
  if count >= limit:
    raise Exception('Twitter rate limit reached. Current count is', count)
