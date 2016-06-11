from django.apps import AppConfig


class EngagementAssignmentConfig(AppConfig):
  name = 'src.domain.engagement_assignment'

  # noinspection PyUnresolvedReferences
  def ready(self):
    import src.domain.engagement_assignment.command_handlers
    import src.domain.engagement_assignment.event_handlers
