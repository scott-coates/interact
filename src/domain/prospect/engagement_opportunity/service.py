from src.apps.relational.topic.service import get_topic_lookups
from src.domain.common import constants
from src.libs.text_utils.token import token_utils
from src.libs.web_utils.url.url_utils import get_unique_urls_from_iterable


def prepare_attrs_from_engagement_opportunity(attrs):
  ret_val = _clean_attrs(attrs)
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


def get_topic_ids_from_engagement_opportunity(attrs, _token_utils=None):
  if not _token_utils: _token_utils = token_utils

  ret_val = []
  text = attrs.get(constants.TEXT)
  text_stemmed = _token_utils.stemmify_string(text)

  topics = get_topic_lookups()

  for topic in topics:
    if topic.stem in text_stemmed:
      ret_val.append(topic.id)

  return ret_val
