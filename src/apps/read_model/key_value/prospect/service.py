import json

from src.apps.read_model.key_value.common import get_read_model_name
from src.domain.common import constants
from src.libs.key_value_utils.key_value_provider import get_key_value_client
from src.libs.key_value_utils.service import push_latest


def save_recent_eo_content(eo_id, eo_attrs, external_id, provider_type, provider_action_type, prospect_id):
  ret_val = None

  text = eo_attrs.get(constants.TEXT)
  if text:
    payload = {
      constants.ID: eo_id, constants.TEXT: text, constants.EXTERNAL_ID: external_id,
      constants.PROVIDER_TYPE: provider_type, constants.PROVIDER_ACTION_TYPE: provider_action_type
    }

    payload_str = json.dumps(payload)
    ret_val = push_latest(get_read_model_name('prospect_recent_eos:{0}', prospect_id), payload_str, 100)

  return ret_val


def get_recent_eo_content(prospect_id):
  kdb = get_key_value_client()

  redis_range = kdb.lrange(get_read_model_name('prospect_recent_eos:{0}', prospect_id), 0, -1)

  ret_val = [json.loads(x.decode()) for x in redis_range]

  return ret_val


def save_recent_prospect_discovery_network_connections_from_eo(eo_attrs, provider_type, prospect_id):
  ret_val = []

  should_add_to_discovery_network = False

  if provider_type == constants.Provider.TWITTER:

    retweet_status = eo_attrs[constants.IS_RETWEET]

    if not retweet_status:
      should_add_to_discovery_network = True

  if should_add_to_discovery_network:

    mentions = eo_attrs.get(constants.MENTIONS)
    if mentions:

      recent_discovery_network = get_recent_prospect_discovery_network(prospect_id)

      for mention in mentions:
        external_id = mention[constants.EXTERNAL_ID]

        existing_recent_connection = next(
            (r for r in recent_discovery_network if
             r[constants.EXTERNAL_ID] == external_id and r[constants.PROVIDER_TYPE] == provider_type
             ), None)

        if existing_recent_connection is None:
          # only add new, distinct connections

          payload = {
            constants.EXTERNAL_ID: external_id,
            constants.PROVIDER_TYPE: provider_type,
          }

          payload_str = json.dumps(payload)
          ret_val.append(
              push_latest(get_read_model_name('prospect_recent_discovery_network:{0}', prospect_id), payload_str, 100)
          )

  return ret_val


def get_recent_prospect_discovery_network(prospect_id):
  kdb = get_key_value_client()

  redis_range = kdb.lrange(get_read_model_name('prospect_recent_discovery_network:{0}', prospect_id), 0, -1)

  ret_val = [json.loads(x.decode()) for x in redis_range]

  return ret_val
