from src.apps.key_value.common import get_app_name
from src.libs.key_value_utils.service import record_rate_limit
from src.libs.social_utils.providers.twitter import twitter_search_utils, twitter_client_service


def search_twitter_by_user(screen_name, _search=twitter_search_utils, **kwargs):
  ret_val = _search.search_twitter_by_user(screen_name, **kwargs)
  _record_twitter_api_call()
  return ret_val


def search_twitter_by_keywords(keyword, _twitter_client_service=twitter_client_service, **kwargs):
  ret_val = _twitter_client_service.search_twitter_by_keywords(keyword, **kwargs)
  _record_twitter_api_call()
  return ret_val


def _record_twitter_api_call():
  record_rate_limit(get_app_name('twitter_api_call'), 15 * 60)
