from django.apps import AppConfig


class KeyValueConfig(AppConfig):
  name = 'src.apps.key_value'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.key_value.prospect.event_handlers
