from src.domain.topic.models import ActiveTATopicOption


def get_active_ta_topic_options():
  active_topics = ActiveTATopicOption.objects.all()
  return active_topics


def get_ta_topic_option(ta_topic_option_id):
  return ActiveTATopicOption.objects.get(id=ta_topic_option_id)
