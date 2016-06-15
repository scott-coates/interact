import logging

from src.libs.key_value_utils.key_value_provider import get_key_value_client

logger = logging.getLogger(__name__)


def save_active_client(client_id):
  kdb = get_key_value_client()
  ret_val = kdb.sadd('active_clients', client_id)
  return ret_val


def get_active_client_ids():
  kdb = get_key_value_client()
  # turn bytes into str
  ret_val = map(lambda m: m.decode(), kdb.smembers('active_clients'))
  return ret_val
