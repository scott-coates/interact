import logging

from src.apps.engagement_discovery.providers.twitter.tasks import discover_engagement_opportunities_task, \
  discover_engagement_opportunities_from_profile_task
from src.domain.common import constants

logger = logging.getLogger(__name__)


def discover_engagement_opportunities():
  discover_engagement_opportunities_task.delay()


def discover_engagement_opportunities_from_profile(external_id, provider_type):
  if provider_type == constants.Provider.TWITTER:
    discover_engagement_opportunities_from_profile_task.delay(external_id)
