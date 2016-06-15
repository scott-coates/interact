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


def save_client_topic_lookup(id, stem):
  kdb = get_key_value_client()
  ret_val = kdb.hset('client_topic_lookup:{0}'.format(id), 'stem', stem)
  return ret_val


def save_client_topic_stem(id, topic_id):
  kdb = get_key_value_client()
  stem = kdb.hget('client_topic_lookup:{0}'.format(topic_id), 'stem')
  ret_val = kdb.sadd('client_topic_stems:{0}'.format(id), stem)
  return ret_val


def get_client_topic_stems(id):
  kdb = get_key_value_client()
  # turn bytes into str
  ret_val = map(lambda m: m.decode(), kdb.smembers('client_topic_stems:{0}'.format(id)))
  return ret_val
