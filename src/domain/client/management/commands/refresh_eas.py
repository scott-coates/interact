from django.core.management.base import NoArgsCommand
from src.domain.client.tasks import refresh_assignments_for_clients_task


class Command(NoArgsCommand):
  def handle_noargs(self, **options):
    refresh_assignments_for_clients_task.delay()
