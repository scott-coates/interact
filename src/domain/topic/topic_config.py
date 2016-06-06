from django.apps import AppConfig


class TopicConfig(AppConfig):
  name = 'src.domain.topic'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.topic.command_handlers
    import src.domain.topic.event_handlers
