from django.dispatch import receiver

from src.domain.engagement_assignment.commands import CreateEA
from src.domain.engagement_assignment.entities import EngagementAssignment
from src.libs.common_domain import aggregate_repository


@receiver(CreateEA.command_signal)
def create_ea(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  ea = EngagementAssignment.from_attrs(**command.data)
  _aggregate_repository.save(ea, -1)

  return ea
