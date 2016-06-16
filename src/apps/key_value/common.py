_kv_prefix = 'read_model'


def get_key_name(key_name, *args, **kwargs):
  key_name = key_name.format(*args, **kwargs)

  ret_val = '{0}:{1}'.format(_kv_prefix, key_name)

  return ret_val
