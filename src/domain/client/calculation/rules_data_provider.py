from src.apps.read_model.relational.client.service import get_client_ea_lookup
from src.domain.common import constants
from src.libs.text_utils.filter import profanity_filter


def provide_rules_data(client_id):
  ret_val = {
    constants.PROFANITY_FILTER_WORDS: profanity_filter.bad_words,
    constants.CLIENT_ID: client_id
  }

  client = get_client_ea_lookup(client_id)

  client_keywords = _provide_keywords(client)
  ret_val.update(client_keywords)

  locations = client.ta_attrs.get(constants.LOCATIONS)
  if locations:
    ret_val[constants.LOCATIONS] = locations

  return ret_val


def _provide_keywords(client):
  ret_val = {}

  ret_val[constants.TOPICS] = {
    v[constants.NAME]: {
      constants.RELEVANCE: v[constants.RELEVANCE],
      constants.ID: k,
    } for k, v in client.ta_topics.items() if v[constants.RELEVANCE] > 0
    }

  return ret_val
