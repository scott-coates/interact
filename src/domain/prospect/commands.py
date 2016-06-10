from src.libs.common_domain.command_signal import CommandSignal
from src.libs.python_utils.objects.object_utils import initializer


class CreateProspect():
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, attrs):
    pass


class CreateProfile():
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, prospect_id, provider_external_id, provider_type, attrs):
    pass
