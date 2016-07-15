import logging

from src.apps.key_value.common import get_read_model_name
from src.libs.key_value_utils.key_value_provider import get_key_value_client

logger = logging.getLogger(__name__)


def save_active_client(client_id):
  kdb = get_key_value_client()
  ret_val = kdb.sadd(get_read_model_name('active_clients'), client_id)
  return ret_val


def get_active_client_ids():
  kdb = get_key_value_client()
  # turn bytes into str
  ret_val = map(lambda m: m.decode(), kdb.smembers(get_read_model_name('active_clients')))
  return ret_val


def save_client_assigned_prospect(client_id, prospect_id):
  kdb = get_key_value_client()
  ret_val = kdb.incr(get_read_model_name('client_assigned_prospects:{0}:{1}', client_id, prospect_id))
  return ret_val


def get_client_assigned_prospect_count(client_id, prospect_id):
  ret_val = 0
  kdb = get_key_value_client()

  count = kdb.get(get_read_model_name('client_assigned_prospects:{0}:{1}', client_id, prospect_id))
  if count:
    ret_val = int(count)

  return ret_val


def mark_ea_batch_to_be_processed(client_id, batch_id, total_assignments_count):
  kdb = get_key_value_client()
  ret_val = kdb.set(get_read_model_name('client_assignment_batch:{0}:{1}', client_id, batch_id), total_assignments_count)
  return ret_val


def clear_ea_batch_to_be_processed(client_id, batch_id):
  kdb = get_key_value_client()
  ret_val = kdb.delete(get_read_model_name('client_assignment_batch:{0}:{1}', client_id, batch_id))
  return ret_val


def get_ea_batch_to_be_processed(client_id, batch_id):
  kdb = get_key_value_client()
  ret_val = int(kdb.get(get_read_model_name('client_assignment_batch:{0}:{1}', client_id, batch_id)))
  return ret_val
