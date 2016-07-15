from src.libs.key_value_utils.key_value_provider import get_key_value_client


# http://redis.io/commands/INCR#pattern-rate-limiter-2
def record_rate_limit(key_name, expiration):
  kdb = get_key_value_client()
  if kdb.exists(key_name):
    # The RPUSHX command only pushes the element if the key already exists. Prevents leaked keys.
    ret_val = kdb.rpushx(key_name, True)
  else:
    pipe = kdb.pipeline()
    pipe.rpush(key_name, True)
    pipe.expire(key_name, expiration)
    ret_val = pipe.execute()

  return ret_val


def get_rate_limit_count(key_name):
  kdb = get_key_value_client()

  ret_val = kdb.llen(key_name)

  return ret_val
