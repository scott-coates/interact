from src.libs.common_domain.command_signal import CommandSignal
from src.libs.common_domain.domain_command import DomainCommand
from src.libs.python_utils.objects.object_utils import initializer


class CreateProspect(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, attrs):
    pass


class AddProfile(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, provider_external_id, provider_type, attrs):
    pass
