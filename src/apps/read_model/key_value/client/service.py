import logging

from flask import json

from src.apps.read_model.key_value.common import get_read_model_name
from src.domain.common import constants
from src.libs.key_value_utils.key_value_provider import get_key_value_client
from src.libs.key_value_utils.service import push_latest

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
  ret_val = kdb.set(get_read_model_name('client_assignment_batch:{0}:{1}', client_id, batch_id),
                    total_assignments_count)
  return ret_val


def clear_ea_batch_to_be_processed(client_id, batch_id):
  kdb = get_key_value_client()
  ret_val = kdb.delete(get_read_model_name('client_assignment_batch:{0}:{1}', client_id, batch_id))
  return ret_val


def get_ea_batch_to_be_processed(client_id, batch_id):
  kdb = get_key_value_client()
  ret_val = int(kdb.get(get_read_model_name('client_assignment_batch:{0}:{1}', client_id, batch_id)))
  return ret_val


def save_client_recent_engagement_assignment_scores(client_id, ea):
  score_attrs = ea[constants.SCORE_ATTRS]
  score_key = score_attrs[constants.SCORE]
  score_attrs_sub_key = score_key[constants.SCORE_ATTRS]

  payload = {k: {constants.COUNT: v[constants.COUNT]} for k, v in score_attrs_sub_key.items()}

  payload_str = json.dumps(payload)

  ret_val = push_latest(get_read_model_name('client_recent_ea_scores:{0}', client_id), payload_str, 100)

  return ret_val


def get_client_recent_engagement_assignment_scores(client_id):
  kdb = get_key_value_client()

  redis_range = kdb.lrange(get_read_model_name('client_recent_ea_scores:{0}', client_id), 0, -1)

  ret_val = [json.loads(x.decode()) for x in redis_range]

  return ret_val
