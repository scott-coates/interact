from django.apps import AppConfig


class GeoConfig(AppConfig):
  name = 'src.apps.geo'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.geo.event_handlers
