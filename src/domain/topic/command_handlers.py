from django.dispatch import receiver

from src.domain.topic.commands import CreateTopic
from src.domain.topic.entities import Topic
from src.libs.common_domain import aggregate_repository


@receiver(CreateTopic.command_signal)
def create_user(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  topic = Topic.from_attrs(**command.data)
  _aggregate_repository.save(topic, -1)

  return topic
