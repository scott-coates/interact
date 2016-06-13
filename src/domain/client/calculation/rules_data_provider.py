from src.domain.common import constants
from src.libs.text_utils.filter import profanity_filter


def provide_rules_data(client_id, assignment_attrs):
  ret_val = {constants.PROFANITY_FILTER_WORDS: profanity_filter.bad_words}
  return ret_val
