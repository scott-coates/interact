from django.apps import AppConfig


class ProspectConfig(AppConfig):
  name = 'src.domain.prospect'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.prospect.command_handlers
    import src.domain.prospect.event_handlers
