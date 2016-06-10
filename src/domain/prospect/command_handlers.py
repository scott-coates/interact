from django.dispatch import receiver

from src.domain.prospect.commands import CreateProspect
from src.domain.prospect.entities import Prospect
from src.libs.common_domain import aggregate_repository


@receiver(CreateProspect.command_signal)
def create_user(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  data = command.__dict__

  topic = Prospect.from_attrs(**data)
  _aggregate_repository.save(topic, -1)

  return topic
