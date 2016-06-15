from django.apps import AppConfig


class AssignmentDeliveryConfig(AppConfig):
  name = 'src.apps.assignment_delivery'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.apps.assignment_delivery.event_handlers
