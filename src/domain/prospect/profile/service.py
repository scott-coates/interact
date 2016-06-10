from src.domain.common import constants
from src.domain.prospect.profile.providers.twitter import twitter_profile_service


def get_profile_attrs_from_provider(profile_external_id, provider_type):
  if provider_type == constants.Provider.TWITTER:
    ret_val = twitter_profile_service.get_twitter_profile_attrs(profile_external_id)
  else:
    raise Exception('Invalid provider type')

  ret_val = _clean_attrs(ret_val)

  return ret_val


def _clean_attrs(attrs):
  websites = attrs.get(constants.WEBSITES)

  if websites:
    # get unique urls from iterable
    websites = list(set(websites))
    ret_val = dict(attrs, **{constants.WEBSITES: websites})

  else:
    ret_val = attrs

  return ret_val
