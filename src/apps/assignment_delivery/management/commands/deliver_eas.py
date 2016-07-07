from django.core.management.base import NoArgsCommand

from src.apps.assignment_delivery.tasks import deliver_assignments_for_clients_task


class Command(NoArgsCommand):
  def handle_noargs(self, **options):
    deliver_assignments_for_clients_task.delay()
