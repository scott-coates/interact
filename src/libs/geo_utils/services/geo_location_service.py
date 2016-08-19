import logging

from pygeocoder import Geocoder, GeocoderError

from src.libs.geo_utils.complete_address import CompleteAddress
from src.libs.geo_utils.exceptions import GeocodeError
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)

_geocoder = Geocoder()


def _get_address_component(address_components, component):
  ret_val = next((x['short_name'] for x in address_components if component in x['types']), None)
  return ret_val


def perform_geo_address_search(address_str):
  geo_log_message = (
    "Performing geo search. address_str: %s",
    address_str
  )

  with log_wrapper(logger.debug, *geo_log_message):
    try:
      results = _geocoder.geocode(address_str)
    except GeocoderError as e:
      raise GeocodeError('invalid address', address_str).with_traceback(e.__traceback__)

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
