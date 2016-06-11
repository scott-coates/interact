from src.libs.key_value_utils.key_value_provider import get_key_value_client


def save_eo_topic_set(eo_id, topic_id):
  kdb = get_key_value_client()

  ret_val = kdb.sadd('eo_topics:{0}'.format(eo_id), topic_id)

  return ret_val


def eo_contains_topic(eo_id, topic_id):
  kdb = get_key_value_client()

  ret_val = kdb.sismember('eo_topics:{0}'.format(eo_id), topic_id)

  return ret_val
