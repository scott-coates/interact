from src.domain.common import constants
from src.domain.topic import service as topic_service
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


def get_topic_ids_from_engagement_opportunity_attrs(attrs, _topic_service=None):
  if not _topic_service: _topic_service = topic_service
  text = attrs.get(constants.TEXT)
  ret_val = _topic_service.get_topic_ids_from_text(text)
  return ret_val
