from django.apps import AppConfig


class EngagementDiscoveryConfig(AppConfig):
  name = 'src.apps.engagement_discovery'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.engagement_discovery.event_handlers
