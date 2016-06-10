from src.domain.common import constants
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
