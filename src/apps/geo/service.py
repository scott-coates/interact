from src.apps.key_value.common import get_app_name
from src.libs.geo_utils.complete_address import CompleteAddress
from src.libs.geo_utils.services import geo_location_service
from src.libs.key_value_utils.key_value_provider import get_key_value_client
from src.libs.text_utils.formatting.text_formatter import only_alpha_numeric


def get_geocoded_address_dict(address_str):
  return dict(get_geocoded_address(address_str)._asdict())


def get_geocoded_address(address_str, _geo_service=None):
  if not _geo_service: _geo_service = geo_location_service

  cached = _get_cached_geocoded_address(address_str)
  if cached:
    ret_val = cached
  else:
    geocoded_address = _geo_service.perform_geo_address_search(address_str)
    _set_cached_geocoded_address(address_str, geocoded_address._asdict())
    ret_val = geocoded_address

  return ret_val


def _get_cached_geocoded_address(address_str):
  ret_val = None
  address_key = _get_address_key(address_str)

  kdb = get_key_value_client()

  geocoded_address = kdb.hgetall(address_key)

  if geocoded_address:
    geocoded_address = dict(map(lambda m: (m[0].decode(), m[1].decode()), geocoded_address.items()))
    geocoded_address['lat'] = float(geocoded_address['lat'])
    geocoded_address['lng'] = float(geocoded_address['lng'])
    ret_val = CompleteAddress(**geocoded_address)

  return ret_val


def _set_cached_geocoded_address(address_str, geocoded_address_dict):
  address_key = _get_address_key(address_str)

  kdb = get_key_value_client()

  kdb.hmset(address_key, geocoded_address_dict)


def _get_address_key(address_str):
  address_key = only_alpha_numeric(address_str).lower()
  address_key = get_app_name('geo_lookup:{0}', address_key)
  return address_key
