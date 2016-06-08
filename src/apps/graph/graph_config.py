from django.apps import AppConfig

class GraphConfig(AppConfig):
  name = 'src.apps.graph'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.graph.client.event_handlers
    import src.apps.graph.topic.event_handlers

