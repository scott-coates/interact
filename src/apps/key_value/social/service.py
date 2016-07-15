import logging

from src.apps.key_value.common import get_app_name
from src.libs.key_value_utils.key_value_provider import get_key_value_client
from src.libs.key_value_utils.service import record_rate_limit

logger = logging.getLogger(__name__)


def record_twitter_search():
  ret_val = record_rate_limit(get_app_name('twitter_search'), 15 * 60)
  return ret_val


def get_twitter_search_count():
  kdb = get_key_value_client()
  ret_val = kdb.llen(get_app_name('twitter_search'))
  return ret_val
