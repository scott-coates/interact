import logging

from src.apps.relational.topic.models import TopicLookup

logger = logging.getLogger(__name__)


def save_topic_lookup(id, name, stem):
  topic, _ = TopicLookup.objects.update_or_create(id=id, defaults=dict(name=name, stem=stem))

  return topic


def get_topic_lookup(id):
  return TopicLookup.objects.get(id=id)


def get_topic_lookups():
  return TopicLookup.objects.all()
