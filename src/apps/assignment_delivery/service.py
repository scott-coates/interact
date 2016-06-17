from src.libs.analytics_utils.providers.keen import keen_client_service
from src.apps.relational.client.service import get_prospect_ea_lookup, get_profile_ea_lookups_by_prospect_id, \
  get_eo_ea_lookup
from src.domain.common import constants


def deliver_ea(prospect_id, ea_data):
  event_data = {}

  prospect = get_prospect_ea_lookup(prospect_id)
  profiles = get_profile_ea_lookups_by_prospect_id(prospect_id)
  profile = profiles[0]

  event_data[constants.NAME] = _get_value(constants.NAMES, prospect.attrs)
  event_data[constants.BIO] = _get_value(constants.BIOS, prospect.attrs)

  event_data[constants.URL] = _get_value(constants.URL, profile.profile_attrs)
  event_data[constants.EO] = _get_value(constants.URL, profile.profile_attrs)

  event_data[constants.SCORE] = _get_value(constants.SCORE, ea_data)

  assigned_entities = []
  for assignment_attr, assigned_entity_ids in ea_data[constants.ATTRS].items():
    for id in assigned_entity_ids:
      if assignment_attr == constants.EO_IDS:
        eo_ea_lookup = get_eo_ea_lookup(id)
        assigned_entities.append(eo_ea_lookup.eo_attrs)
  if assigned_entities:
    event_data[constants.EO] = [_get_value(constants.TEXT, ae) for ae in assigned_entities]

  return keen_client_service.send_event('engagement_assigned', event_data)


def _get_value(key, data):
  val = data.get(key, 'Unknown')

  if isinstance(val, list):
    if len(val):
      val = val[0]

  return val
