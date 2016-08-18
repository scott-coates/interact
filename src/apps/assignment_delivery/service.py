import json

from src.apps.read_model.relational.client.service import get_prospect_ea_lookup, \
  get_profile_ea_lookups_by_prospect_id, \
  get_eo_ea_lookup, save_delivered_ea
from src.domain.common import constants
from src.libs.analytics_utils.providers.keen import keen_client_service


def deliver_ea_to_analytics_service(ea_data):
  event_data = _convert_ea_data_to_deliverable(ea_data)

  event_data[constants.ASSIGNED_ENTITIES] = json.dumps(event_data[constants.ASSIGNED_ENTITIES])

  return keen_client_service.send_event('engagement_assigned', event_data)


def deliver_ea_to_read_model(ea_data, batch_id):
  event_data = _convert_ea_data_to_deliverable(ea_data)

  event_data[constants.SCORE_ATTRS] = _get_value(ea_data, constants.SCORE_ATTRS)

  ea_id = event_data.pop(constants.ID)
  event_data['ea_id'] = ea_id
  event_data['batch_id'] = batch_id

  return save_delivered_ea(**event_data)


def _convert_ea_data_to_deliverable(ea_data):
  ret_val = {}

  prospect_id = ea_data[constants.PROSPECT_ID]
  prospect = get_prospect_ea_lookup(prospect_id)
  profiles = get_profile_ea_lookups_by_prospect_id(prospect_id)
  profile = profiles[0]

  ret_val[constants.PROSPECT_ID] = prospect_id
  ret_val[constants.NAME] = _get_value(prospect.attrs, constants.NAMES)
  ret_val[constants.BIO] = _get_value(prospect.attrs, constants.BIOS)
  ret_val[constants.LOCATION] = _get_value(prospect.attrs, constants.LOCATIONS, 'formatted_address')

  ret_val[constants.URL] = _get_value(profile.profile_attrs, constants.URL)

  ret_val[constants.SCORE] = _get_value(ea_data, constants.SCORE)

  ret_val[constants.ID] = _get_value(ea_data, constants.ID)

  assigned_entities_to_deliver = []

  for assignment_entity_attr in ea_data[constants.SCORE_ATTRS][constants.ASSIGNED_ENTITIES][constants.DATA]:
    if assignment_entity_attr[constants.ASSIGNED_ENTITY_TYPE] == constants.EO:
      eo_ea_lookup = get_eo_ea_lookup(assignment_entity_attr[constants.ID])

      score_attrs = {
        constants.EO_TOPIC: assignment_entity_attr[constants.SCORE_ATTRS][constants.EO_TOPIC][
          constants.SCORE_ATTRS]
      }

      if constants.EO_ENGAGEMENT in assignment_entity_attr[constants.SCORE_ATTRS]:
        score_attrs[constants.EO_ENGAGEMENT] = assignment_entity_attr[constants.SCORE_ATTRS][constants.EO_ENGAGEMENT]

    else:
      raise Exception('invalid type')

    assigned_entities_to_deliver.append(
        {
          constants.ID: eo_ea_lookup.id,
          constants.ATTRS: eo_ea_lookup.eo_attrs,
          constants.SCORE_ATTRS: score_attrs
        }
    )

  ret_val[constants.ASSIGNED_ENTITIES] = [
    {
      constants.ID: _get_value(ae, constants.ID),
      constants.TEXT: _get_value(ae, constants.ATTRS, constants.TEXT),
      constants.SCORE_ATTRS: _get_value(ae, constants.SCORE_ATTRS)
    }
    for ae in
    assigned_entities_to_deliver
    ]

  return ret_val


def _get_value(data, *keys):
  for key in keys:
    val = data.get(key, 'Unknown')

    if isinstance(val, list):
      if len(val):
        val = val[0]

    if isinstance(val, dict):
      key_tail = keys[1:]
      if key_tail:
        val = _get_value(val, *key_tail)

    return val
