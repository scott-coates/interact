from django.core.management.base import BaseCommand

from src.libs.common_domain import event_store


class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('event_names', nargs='*', default=None)

  def handle(self, *args, **options):
    event_store.replay_events(options['event_names'])
