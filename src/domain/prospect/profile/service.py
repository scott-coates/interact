from src.domain.common import constants
from src.domain.prospect.profile.providers.twitter import twitter_profile_service
from src.domain.topic import service as topic_service
from src.libs.web_utils.url.url_utils import get_unique_urls_from_iterable


def get_profile_attrs_from_provider(external_id, provider_type):
  if provider_type == constants.Provider.TWITTER:
    ret_val = twitter_profile_service.get_twitter_profile_attrs(external_id)
  else:
    raise Exception('Invalid provider type')

  ret_val = _clean_attrs(ret_val)

  return ret_val


def get_topic_ids_from_profile_attrs(attrs, _topic_service=None):
  if not _topic_service: _topic_service = topic_service
  text = attrs.get(constants.TEXT)
  ret_val = _topic_service.get_topic_ids_from_text(text)
  return ret_val


def _clean_attrs(attrs):
  websites = attrs.get(constants.WEBSITES)

  if websites:
    # get unique urls from iterable
    websites = get_unique_urls_from_iterable(websites)
    ret_val = dict(attrs, **{constants.WEBSITES: websites})

  else:
    ret_val = attrs

  return ret_val
