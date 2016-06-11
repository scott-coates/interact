from django.dispatch import receiver

from src.domain.prospect.commands import CreateProspect, AddProfile, AddEO, AddTopicToEO
from src.domain.prospect.entities import Prospect
from src.libs.common_domain import aggregate_repository


@receiver(CreateProspect.command_signal)
def create_prospect(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  topic = Prospect.from_attrs(**command.data)
  _aggregate_repository.save(topic, -1)

  return topic


@receiver(AddProfile.command_signal)
def add_profile(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  command = kwargs['command']
  prospect_id = kwargs['aggregate_id']

  prospect = _aggregate_repository.get(Prospect, prospect_id)
  version = prospect.version
  prospect.add_profile(**command.data)
  _aggregate_repository.save(prospect, version)


@receiver(AddEO.command_signal)
def add_eo(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  command = kwargs['command']
  prospect_id = kwargs['aggregate_id']

  prospect = _aggregate_repository.get(Prospect, prospect_id)
  version = prospect.version
  prospect.add_eo(**command.data)
  _aggregate_repository.save(prospect, version)

@receiver(AddTopicToEO.command_signal)
def add_topic_to_eo(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  command = kwargs['command']
  prospect_id = kwargs['aggregate_id']

  prospect = _aggregate_repository.get(Prospect, prospect_id)
  version = prospect.version
  prospect.add_topic_to_eo(**command.data)
  _aggregate_repository.save(prospect, version)
