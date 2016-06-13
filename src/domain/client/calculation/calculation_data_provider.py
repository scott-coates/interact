from src.domain.common import constants
from src.libs.text_utils.filter import profanity_filter


def provide_stemmed_keywords(client, assigned_calc_objects):
  ret_val = []

  for calc_obj in assigned_calc_objects:

    assigned_entity = calc_obj.assigned_entity

    # todo don't check type - always pass in id?
    if isinstance(assigned_entity, EngagementOpportunity):
      eo = assigned_entity
      topic_ids = list(eo.topics.values_list('topic_type_id', flat=True))
    else:
      raise Exception("Invalid assigned type")

    for ta_topic in client.ta_topics.exclude(topic_type_id__in=topic_ids):

      # store the `root` topic's stemmed value
      ret_val.append(ta_topic.topic_type.snowball_stem)

      # now iterate through each of the sub topics and get their stem too
      for keywords_topic in ta_topic.topic_type.subtopics.filter(category_type=TopicCategoryEnum.keywords):
        ret_val.append(keywords_topic.subtopic_attrs[constants.SNOWBALL_STEM])

  return list(set(ret_val))


def provide_calculation_data():
  ret_val = {constants.PROFANITY_FILTER_WORDS: profanity_filter.bad_words}

  def _get_calc_data(assignment_attrs, client_id, _calc_data_provider=None):
    if not _calc_data_provider: _calc_data_provider = calculation_data_provider

  ret_val = _calc_data_provider.provide_calculation_data()

  # todo get client's import bio, websites, etc from here too - lets not use a custom client class
  stemmed_keywords = _calc_data_provider.provide_stemmed_keywords(client, assigned_calc_objects)
  ret_val[constants.STEMMED_TA_TOPIC_KEYWORDS] = stemmed_keywords

  client_uid = _calc_data_provider.provide_client_uid(client)
  ret_val[constants.CLIENT_UID] = client_uid

  ret_val[constants.PROFANITY_FILTER_WORDS] = _calc_data_provider.provide_profanity_word_list()

  return profanity_filter.bad_words
