from src.apps.relational.topic import service as topic_read_service
from src.libs.text_utils.formatting.text_formatter import only_alpha_numeric
from src.libs.text_utils.token import token_utils


def get_topic_ids_from_text(text, _topic_read_service=None, _token_utils=None):
  if not _topic_read_service: _topic_read_service = topic_read_service
  if not _token_utils: _token_utils = token_utils

  ret_val = []
  text_stemmed = _token_utils.stemmify_string(text)

  text_alnum = only_alpha_numeric(text_stemmed)
  text_words = [only_alpha_numeric(x) for x in text_stemmed.split()]

  topics = _topic_read_service.get_topic_lookups()

  for topic in topics:

    if ' ' in topic.stem:
      if only_alpha_numeric(topic.stem) in text_alnum:
        ret_val.append(topic.id)
      else:
        # collapsed_stem is already only_alpha_numeric
        if topic.collapsed_stem in text_alnum:
          ret_val.append(topic.id)
    elif only_alpha_numeric(topic.stem) in text_words:
      ret_val.append(topic.id)

  return ret_val


def get_topic_stems(name, _token_utils=None):
  if not _token_utils: _token_utils = token_utils
  topic_stem = _token_utils.stemmify_string(name)
  collapsed_topic_stem = _token_utils.stemmify_string(only_alpha_numeric(name))

  return topic_stem, collapsed_topic_stem
