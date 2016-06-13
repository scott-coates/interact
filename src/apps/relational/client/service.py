import logging

from src.apps.relational.client.models import ActiveTATopicOption, ActiveClient
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


def get_active_ta_topic_options():
  active_topics = ActiveTATopicOption.objects.all()
  return active_topics


def get_ta_topic_option(ta_topic_option_id):
  return ActiveTATopicOption.objects.get(id=ta_topic_option_id)


def save_active_ta_topic_option(id, option_name, option_type, option_attrs, ta_topic_id, topic_id, client_id):
  at, _ = ActiveTATopicOption.objects.update_or_create(
      id=id, defaults=dict(
          option_name=option_name, option_type=option_type,
          option_attrs=option_attrs, ta_topic_id=ta_topic_id,
          topic_id=topic_id, client_id=client_id
      )
  )
  return at


def save_active_client(id):
  ac, _ = ActiveClient.objects.update_or_create(id=id)
  return ac


def get_active_clients():
  active_clients = ActiveClient.objects.all()
  return active_clients

