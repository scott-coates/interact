from django.core.management.base import NoArgsCommand
from src.apps.engagement_discovery.tasks import discover_engagement_opportunities_task


class Command(NoArgsCommand):
  def handle_noargs(self, **options):
    discover_engagement_opportunities_task.delay()
