from src.libs.common_domain.command_signal import CommandSignal
from src.libs.common_domain.domain_command import DomainCommand
from src.libs.python_utils.objects.object_utils import initializer


class CreateProspect(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, attrs):
    pass


class MarkProspectAsDuplicate(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, existing_prospect_id):
    pass


class ConsumeDuplicateProspect(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, duplicate_prospect_id):
    pass


class AddProfile(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, external_id, provider_type):
    pass


class AddEO(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, external_id, attrs, provider_type,
               provider_action_type, created_date, profile_id, ):
    pass


class AddTopicToEO(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, eo_id, topic_id):
    pass
