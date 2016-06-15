from itertools import chain

from src.apps.relational.client.service import get_client_ea_lookup
from src.domain.common import constants
from src.libs.text_utils.filter import profanity_filter


def provide_rules_data(client_id, assigned_calc_objects):
  ret_val = {
    constants.PROFANITY_FILTER_WORDS: profanity_filter.bad_words
  }

  client = get_client_ea_lookup(client_id)

  client_keywords = _provide_stemmed_keywords(client, assigned_calc_objects)
  if client_keywords:
    ret_val[constants.KEYWORDS] = client_keywords

  locations = client.ta_attrs.get(constants.LOCATIONS)
  if locations:
    ret_val[constants.LOCATIONS] = locations

  return ret_val


def _provide_stemmed_keywords(client, assigned_calc_objects):
  topic_ids = chain.from_iterable(c.topic_ids for c in assigned_calc_objects)

  available_keywords = [v for k, v in client.ta_topics.items() if k not in topic_ids]

  return list(set(available_keywords))
