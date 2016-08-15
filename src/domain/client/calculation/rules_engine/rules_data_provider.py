from src.apps.read_model.key_value.prospect.service import get_recent_eo_content
from src.apps.read_model.relational.client.service import get_client_ea_lookup
from src.domain.client.calculation.processing.data_processor import get_comparative_text_from_tweet
from src.domain.common import constants
from src.libs.text_utils.filter import profanity_filter


def provide_rules_data(client_id, prospect_id):
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

  recent_eos = _get_recent_eos(prospect_id)
  if recent_eos:
    ret_val[constants.RECENT_EOS] = recent_eos

  return ret_val


def _provide_keywords(client):
  ret_val = {}

  ret_val[constants.TOPICS] = {
    v[constants.NAME]: {
      constants.ID: k,
    } for k, v in client.ta_topics.items() if v[constants.RELEVANCE] > 0
    }

  return ret_val


def _get_recent_eos(prospect_id):
  ret_val = []
  recent_eos = get_recent_eo_content(prospect_id)

  for re in recent_eos:
    if re[constants.PROVIDER_ACTION_TYPE] == constants.ProviderAction.TWITTER_TWEET:
      comparative_tweet_text = get_comparative_text_from_tweet(re[constants.TEXT])
      ret_val.append({
        constants.ID: re[constants.ID],
        constants.COMPARATIVE_TEXT: comparative_tweet_text,
        constants.SIMILAR_EOS: [],
      })

  return ret_val
