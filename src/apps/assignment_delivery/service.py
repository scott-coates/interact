from src.apps.relational.client.service import get_prospect_ea_lookup, get_profile_ea_lookups_by_prospect_id, \
  get_eo_ea_lookup
from src.domain.common import constants
from src.libs.analytics_utils.providers.keen import keen_client_service


def deliver_ea(ea_data):
  event_data = {}

  prospect_id = ea_data[constants.PROSPECT_ID]
  prospect = get_prospect_ea_lookup(prospect_id)
  profiles = get_profile_ea_lookups_by_prospect_id(prospect_id)
  profile = profiles[0]

  event_data[constants.PROSPECT_ID] = prospect_id
  event_data[constants.NAME] = _get_value(prospect.attrs, constants.NAMES)
  event_data[constants.BIO] = _get_value(prospect.attrs, constants.BIOS)
  event_data[constants.LOCATION] = _get_value(prospect.attrs, constants.LOCATIONS, 'formatted_address')

  event_data[constants.URL] = _get_value(profile.profile_attrs, constants.URL)
  event_data[constants.EO] = _get_value(profile.profile_attrs, constants.URL)

  event_data[constants.SCORE] = _get_value(ea_data, constants.SCORE)
  event_data[constants.ID] = _get_value(ea_data, constants.ID)

  assigned_entities_to_deliver = []

  for assignment_entity_attr in ea_data[constants.SCORE_ATTRS][constants.ASSIGNED_ENTITIES]:
    if assignment_entity_attr[constants.ASSIGNED_ENTITY_TYPE] == constants.EO:
      eo_ea_lookup = get_eo_ea_lookup(assignment_entity_attr[constants.ID])
      assigned_entities_to_deliver.append(eo_ea_lookup.eo_attrs)

  if assigned_entities_to_deliver:
    event_data[constants.EO] = [_get_value(ae, constants.TEXT) for ae in assigned_entities_to_deliver]

  return keen_client_service.send_event('engagement_assigned', event_data)


def _get_value(data, *keys):
  for key in keys:
    val = data.get(key, 'Unknown')

    if isinstance(val, list):
      if len(val):
        val = val[0]

    if isinstance(val, dict):
      val = _get_value(val, *keys[1:])

    return val
