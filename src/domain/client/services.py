from src.domain.client.models import ActiveTATopicOption


def save_active_ta_topic_option(id, option_name, option_type, option_attrs, ta_topic_id, topic_id, client_id):
  at, _ = ActiveTATopicOption.objects.update_or_create(
      id=id, defaults=dict(
          option_name=option_name, option_type=option_type,
          option_attrs=option_attrs, ta_topic_id=ta_topic_id,
          topic_id=topic_id, client_id=client_id
      )
  )
  return at
