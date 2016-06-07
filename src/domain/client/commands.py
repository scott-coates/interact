from src.libs.common_domain.command_signal import CommandSignal
from src.libs.python_utils.objects.object_utils import initializer


class CreateClient():
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, name):
    pass


class AssociateWithTopic():
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, topic_id,):
    pass


class AddTopicOption():
  command_signal = CommandSignal()

  @initializer
  def __init__(self, id, name, type, attrs, ta_topic_id ):
    pass
