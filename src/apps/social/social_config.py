from django.apps import AppConfig


class SocialConfig(AppConfig):
  name = 'src.apps.social'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.social.event_handlers
