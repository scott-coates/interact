from src.apps.relational.client.service import get_client_ea_lookup
from src.domain.common import constants
from src.libs.text_utils.filter import profanity_filter


def provide_rules_data(client_id, assignment_attrs):
  client = get_client_ea_lookup(client_id)
  ret_val = {
    constants.PROFANITY_FILTER_WORDS: profanity_filter.bad_words

  }

  locations = client.ta_attrs.get(constants.LOCATIONS)
  if locations:
    ret_val[constants.LOCATIONS] = locations

  return ret_val
