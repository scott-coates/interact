from django.core.exceptions import ObjectDoesNotExist

from src.domain.common import constants
from src.domain.prospect.commands import CreateProspect, AddProfile
from src.domain.prospect.models import ProfileLookupByProvider
from src.domain.prospect.profile.providers.twitter import twitter_profile_service
from src.libs.common_domain import dispatcher
from src.libs.python_utils.id.id_utils import generate_id


def get_prospect_id_from_provider_info_(provider_external_id, provider_type, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  try:
    profile = _get_profile_from_provider_info(provider_external_id, provider_type)
    prospect_id = profile.prospect_id
  except ObjectDoesNotExist:
    # at some point in the future,  we could get initial prospect info from a 3rd party api. We could get email
    # addresses, etc.
    prospect_id = generate_id()
    create_prospect = CreateProspect(prospect_id, None)
    _dispatcher.send_command(-1, create_prospect)

  return prospect_id


def get_profile_id_from_provider_info(prospect_id, provider_external_id, provider_type, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  try:
    profile = _get_profile_from_provider_info(provider_external_id, provider_type)
    profile_id = profile.id

  except ObjectDoesNotExist:

    profile_id = generate_id()

    if provider_type == constants.Provider.TWITTER:
      attrs = twitter_profile_service.get_twitter_profile_data(provider_external_id)
      create_profile = AddProfile(profile_id, provider_external_id, provider_type, attrs)

    else:
      raise Exception('Invalid provider type')

    _dispatcher.send_command(prospect_id, create_profile)

  return profile_id


def save_profile_lookup_by_provider(profile_id, provider_external_id, provider_type, prospect_id):
  profile, _ = ProfileLookupByProvider.objects.update_or_create(
      id=profile_id, defaults=dict(
          provider_external_id=provider_external_id, provider_type=provider_type, prospect_id=prospect_id
      )
  )

  return profile


def _get_profile_from_provider_info(provider_external_id, provider_type):
  return ProfileLookupByProvider.objects.get(provider_external_id=provider_external_id, provider_type=provider_type)
