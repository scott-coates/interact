from src.apps.key_value.common import get_key_name
from src.libs.key_value_utils.key_value_provider import get_key_value_client


def add_prospect_to_deleted_set(prospect_id):
  kdb = get_key_value_client()

  ret_val = kdb.sadd(get_key_name('deleted_prospects'), prospect_id)

  return ret_val


def prospect_is_deleted(prospect_id):
  kdb = get_key_value_client()

  ret_val = kdb.sismember(get_key_name('deleted_prospects'), prospect_id)

  return ret_val
