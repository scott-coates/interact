import logging

from pygeocoder import Geocoder

from src.libs.geo_utils.complete_address import CompleteAddress
from src.libs.key_value_utils.key_value_provider import get_key_value_client
from src.libs.python_utils.logging.logging_utils import log_wrapper
from src.libs.text_utils.formatting.text_formatter import only_alpha_numeric

logger = logging.getLogger(__name__)

_geocoder = Geocoder()


def _get_address_component(address_components, component):
  try:
    ret_val = next(x['short_name'] for x in address_components if component in x['types'])
  except StopIteration:
    ret_val = None

  return ret_val


def get_geocoded_address(address_str):
  return _get_cached_geocoded_address(address_str)


def get_geocoded_address_dict(address_str):
  return dict(get_geocoded_address(address_str)._asdict())


def _get_cached_geocoded_address(address_str):
  address_key = only_alpha_numeric(address_str).lower()
  address_key = 'geo_lookup:{0}'.format(address_key)

  kdb = get_key_value_client()

  geocoded_address = kdb.hgetall(address_key)

  if not geocoded_address:
    geocoded_address = _perform_geo_address_search(address_str)
    kdb.hmset(address_key, geocoded_address._asdict())
  else:
    geocoded_address = dict(map(lambda m: (m[0].decode(), m[1].decode()), geocoded_address.items()))
    geocoded_address['lat'] = float(geocoded_address['lat'])
    geocoded_address['lng'] = float(geocoded_address['lng'])
    geocoded_address = CompleteAddress(**geocoded_address)
  return geocoded_address


def _perform_geo_address_search(address_str):
  geo_log_message = (
    "Performing geo search. address_str: %s",
    address_str
  )

  with log_wrapper(logger.debug, *geo_log_message):
    results = _geocoder.geocode(address_str)

  address_components = results.data[0]['address_components']

  address1 = _get_address_component(address_components, 'street_number')
  if not address1:
    address1 = _get_address_component(address_components, 'route')

  address2 = _get_address_component(address_components, 'subpremise')

  city = _get_address_component(address_components, 'sublocality')
  if not city:
    city = _get_address_component(address_components, 'locality')

  # manhattan is not legally a city, but google geocoder thinks it is.
  if city and city.lower() == 'manhattan': city = 'New York'

  state = _get_address_component(address_components, 'administrative_area_level_1')
  zip_code = _get_address_component(address_components, 'postal_code')
  country = _get_address_component(address_components, 'country')

  return CompleteAddress(results.latitude, results.longitude, address1, address2, city, state,
                         country, zip_code, results.formatted_address)
