import logging

from django_rq import job

from src.apps.engagement_discovery import service
from src.libs.python_utils.logging.logging_utils import log_wrapper

logger = logging.getLogger(__name__)


@job('default')
def discover_engagement_opportunities_task():
  log_message = "Discover opportunity engagements."

  with log_wrapper(logger.debug, log_message):
    return service.discover_engagement_opportunities()
