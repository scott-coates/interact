from src.domain.topic.models import ActiveTATopic


def get_active_ta_topic():
  active_topics = ActiveTATopic.objects.all()
  return active_topics


def get_ta_topic_option(ta_topic_option_id):
  return None
