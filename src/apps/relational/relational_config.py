from django.apps import AppConfig


class RelationalConfig(AppConfig):
  name = 'src.apps.relational'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.relational.client.event_handlers
    import src.apps.relational.prospect.event_handlers
    import src.apps.relational.topic.event_handlers
