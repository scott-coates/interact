from django.conf import settings

from keen.client import KeenClient

client = KeenClient(
    project_id=settings.KEEN_PROJECT_ID,
    write_key=settings.KEEN_WRITE_KEY,
    read_key=settings.KEEN_READ_KEY
)


def get_keen_client():
  return client
