from django.core.exceptions import ObjectDoesNotExist

from src.domain.common import constants
from src.domain.prospect.models import ProfileProspectLookup


def save_prospect_from_provider_info_(profile_external_id, provider_type):
  try:
    profile = _get_profile_from_provider_info(profile_external_id, provider_type)
  except ObjectDoesNotExist:
    # at some point in the future,  we could get initial prospect info from a 3rd party api. We could get email
    # addresses, etc.
    # todo
    pass
  return None


def _get_profile_from_provider_info(profile_external_id, provider_type):
  return ProfileProspectLookup.objects.get(profile_external_id=profile_external_id, provider_type=provider_type)


def save_profile_from_provider_info(prospect_id, profile_external_id, provider_type):
  try:
    profile = _get_profile_from_provider_info(profile_external_id, provider_type)
  except ObjectDoesNotExist:
    if provider_type == constants.Provider.TWITTER:
      profile_attrs = twitter_profile_service.get_twitter_profile_attrs(profile_external_id, **kwargs)

    else:
      raise Exception('Invalid provider type')

  return None
