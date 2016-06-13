from django.core.exceptions import ObjectDoesNotExist

from src.apps.relational.prospect.service import get_profile_lookup_from_provider_info, \
  get_engagement_opportunity_lookup_from_provider_info, get_engagement_opportunity_lookup, get_profile_lookup
from src.domain.prospect.commands import CreateProspect, AddProfile, AddEO, AddTopicToEO
from src.libs.common_domain import dispatcher
from src.libs.python_utils.id.id_utils import generate_id


def populate_prospect_id_from_provider_info_(external_id, provider_type, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  try:
    profile = get_profile_lookup_from_provider_info(external_id, provider_type)
    prospect_id = profile.prospect_id
  except ObjectDoesNotExist:
    # at some point in the future,  we could get initial prospect info from a 3rd party api. We could get email
    # addresses, etc.
    prospect_id = generate_id()
    create_prospect = CreateProspect(prospect_id, {})
    _dispatcher.send_command(-1, create_prospect)

  return prospect_id


def populate_profile_id_from_provider_info(prospect_id, external_id, provider_type, _dispatcher=None):
  if not _dispatcher: _dispatcher = dispatcher

  try:
    profile = get_profile_lookup_from_provider_info(external_id, provider_type)
    # todo i think this is the time to refresh their profile data
    # every tmie we come across their profile, we can see what's new.
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
    eo = get_engagement_opportunity_lookup_from_provider_info(discovery.engagement_opportunity_external_id,
                                                              provider_type)

    eo_id = eo.id

  except ObjectDoesNotExist:

    profile = get_profile_lookup(profile_id)

    eo_id = generate_id()

    create_eo = AddEO(eo_id, discovery.engagement_opportunity_external_id,
                      discovery.engagement_opportunity_attrs,
                      provider_type, discovery.provider_action_type, discovery.created_date,
                      profile_id)

    _dispatcher.send_command(profile.prospect_id, create_eo)

  return eo_id


def add_topic_to_eo(eo_id, topic_id):
  eo = get_engagement_opportunity_lookup(eo_id)

  prospect_id = eo.prospect_id

  add_topic = AddTopicToEO(eo_id, topic_id)

  dispatcher.send_command(prospect_id, add_topic)

  return eo_id
