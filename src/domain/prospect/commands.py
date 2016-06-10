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
  def __init__(self, id, profile_external_id, provider_type):
    pass


class AddEO(DomainCommand):
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, engagement_opportunity_external_id, engagement_opportunity_attrs, provider_type,
               provider_action_type, created_at, profile_id, ):
    pass
