from django.dispatch import receiver

from src.domain.client.commands import CreateClient, AssociateWithTopic, AddTopicOption, AddEA
from src.domain.client.entities import Client
from src.libs.common_domain import aggregate_repository


@receiver(CreateClient.command_signal)
def create_client(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository
  command = kwargs['command']

  client = Client.from_attrs(**command.data)
  _aggregate_repository.save(client, -1)

  return client


@receiver(AssociateWithTopic.command_signal)
def associate_topic(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  command = kwargs['command']
  id = kwargs['aggregate_id']

  client = _aggregate_repository.get(Client, id)
  version = client.version
  client.associate_with_topic(**command.data)
  _aggregate_repository.save(client, version)


@receiver(AddTopicOption.command_signal)
def add_option(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  command = kwargs['command']
  id = kwargs['aggregate_id']

  client = _aggregate_repository.get(Client, id)
  version = client.version
  client.add_topic_option(**command.data)
  _aggregate_repository.save(client, version)


@receiver(AddEA.command_signal)
def create_ea(_aggregate_repository=None, **kwargs):
  if not _aggregate_repository: _aggregate_repository = aggregate_repository

  command = kwargs['command']
  id = kwargs['aggregate_id']

  client = _aggregate_repository.get(Client, id)
  version = client.version
  client.add_ea(**command.data)
  _aggregate_repository.save(client, version)
