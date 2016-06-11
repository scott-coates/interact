from django.core.exceptions import ObjectDoesNotExist

from src.domain.prospect.commands import CreateProspect, AddProfile, AddEO, AddTopicToEO
from src.domain.prospect.models import ProfileLookupByProvider, EngagementOpportunityLookupByProvider
from src.libs.common_domain import dispatcher
from src.libs.python_utils.id.id_utils import generate_id


def populate_prospect_id_from_provider_info_(external_id, provider_type, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  try:
    profile = _get_profile_from_provider_info(external_id, provider_type)
    prospect_id = profile.prospect_id
  except ObjectDoesNotExist:
    # at some point in the future,  we could get initial prospect info from a 3rd party api. We could get email
    # addresses, etc.
    prospect_id = generate_id()
    create_prospect = CreateProspect(prospect_id, None)
    _dispatcher.send_command(-1, create_prospect)

  return prospect_id


def populate_profile_id_from_provider_info(prospect_id, external_id, provider_type, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  try:
    profile = _get_profile_from_provider_info(external_id, provider_type)
    profile_id = profile.id

  except ObjectDoesNotExist:

    profile_id = generate_id()

    create_profile = AddProfile(profile_id, external_id, provider_type)

    _dispatcher.send_command(prospect_id, create_profile)

  return profile_id


def populate_engagement_opportunity_id_from_engagement_discovery(profile_id, engagement_opportunity_discovery_object,
                                                                 _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  discovery = engagement_opportunity_discovery_object
  provider_type = discovery.provider_type

  try:
    eo = _get_engagement_opportunity_from_provider_info(discovery.engagement_opportunity_external_id, provider_type)

    eo_id = eo.id

  except ObjectDoesNotExist:

    profile = _get_profile_from_provider_info(profile_id, provider_type)

    eo_id = generate_id()

    create_eo = AddEO(eo_id, discovery.engagement_opportunity_external_id,
                      discovery.engagement_opportunity_attrs,
                      provider_type, discovery.provider_action_type, discovery.created_at,
                      profile_id)

    _dispatcher.send_command(profile.prospect_id, create_eo)

  return eo_id


def add_topic_to_eo(eo_id, topic_id):
  eo = _get_engagement_opportunity(eo_id)

  prospect_id = eo.prospect_id

  add_topic = AddTopicToEO(eo_id, topic_id)

  dispatcher.send_command(prospect_id, add_topic)

  return eo_id


def save_profile_lookup_by_provider(profile_id, external_id, provider_type, prospect_id):
  profile, _ = ProfileLookupByProvider.objects.update_or_create(
      id=profile_id, defaults=dict(
          external_id=external_id, provider_type=provider_type, prospect_id=prospect_id
      )
  )

  return profile


def save_eo_lookup_by_provider(eo_id, external_id, provider_type, prospect_id):
  eo, _ = EngagementOpportunityLookupByProvider.objects.update_or_create(
      id=eo_id, defaults=dict(
          external_id=external_id, provider_type=provider_type, prospect_id=prospect_id
      )
  )

  return eo


def _get_profile_from_provider_info(external_id, provider_type):
  return ProfileLookupByProvider.objects.get(external_id=external_id, provider_type=provider_type)


def _get_engagement_opportunity_from_provider_info(external_id, provider_type):
  return EngagementOpportunityLookupByProvider.objects.get(
      external_id=external_id, provider_type=provider_type)


def _get_engagement_opportunity(eo_id):
  return EngagementOpportunityLookupByProvider.objects.get(id=eo_id)
