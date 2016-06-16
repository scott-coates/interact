from django.dispatch import receiver

from src.domain.prospect.commands import CreateProspect, AddProfile, AddEO, AddTopicToEO, MarkProspectAsDuplicate, \
  ConsumeDuplicateProspect
from src.domain.prospect.entities import Prospect
from src.libs.common_domain import aggregate_repository


@receiver(CreateProspect.command_signal)
def create_prospect(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  prospect = Prospect.from_attrs(**command.data)
  _aggregate_repository.save(prospect, -1)

  return prospect


@receiver(MarkProspectAsDuplicate.command_signal)
def mark_prospect_as_duplicate(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  command = kwargs['command']
  prospect_id = kwargs['aggregate_id']

  prospect = _aggregate_repository.get(Prospect, prospect_id)
  version = prospect.version
  prospect.mark_as_duplicate(**command.data)
  _aggregate_repository.save(prospect, version)


@receiver(ConsumeDuplicateProspect.command_signal)
def consume_duplicate_prospect(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  command = kwargs['command']
  prospect_id = kwargs['aggregate_id']
  duplicate_prospect_id = command.duplicate_prospect_id

  prospect = _aggregate_repository.get(Prospect, prospect_id)
  duplicate_prospect = _aggregate_repository.get(Prospect, prospect_id)
  version = prospect.version
  prospect.consume_duplicate_prospect(duplicate_prospect)
  _aggregate_repository.save(prospect, version)


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
