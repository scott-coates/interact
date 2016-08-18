import json

from src.apps.key_value.common import get_read_model_name
from src.domain.common import constants
from src.libs.key_value_utils.key_value_provider import get_key_value_client
from src.libs.key_value_utils.service import push_latest


def save_recent_eo_content(eo_id, content, external_id, provider_type, provider_action_type, prospect_id):
  payload = {
    constants.ID: eo_id, constants.TEXT: content, constants.EXTERNAL_ID: external_id,
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


def save_recent_prospect_discovery_network_connection(external_id, provider_type, prospect_id):
  ret_val = None

  recent_discovery_network = get_recent_prospect_discovery_network(prospect_id)

  existing_recent_connection = next((r for r in recent_discovery_network
                                     if r[constants.EXTERNAL_ID] == external_id and
                                     r[constants.PROVIDER_TYPE] == provider_type), None)

  if existing_recent_connection is None:
    # only add new, distinct connections

    payload = {
      constants.EXTERNAL_ID: external_id,
      constants.PROVIDER_TYPE: provider_type,
      constants.PROSPECT_ID: prospect_id
    }

    payload_str = json.dumps(payload)
    ret_val = push_latest(get_read_model_name('prospect_recent_discovery_network:{0}', prospect_id), payload_str, 100)

  return ret_val


def get_recent_prospect_discovery_network(prospect_id):
  kdb = get_key_value_client()

  redis_range = kdb.lrange(get_read_model_name('prospect_recent_discovery_network:{0}', prospect_id), 0, -1)

  ret_val = [json.loads(x.decode()) for x in redis_range]

  return ret_val
