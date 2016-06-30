import logging

from src.apps.engagement_discovery.providers.twitter import twitter_engagement_discovery_provider
from src.domain.common import constants

logger = logging.getLogger(__name__)


def discover_engagement_opportunities():
  twitter_engagement_discovery_provider.discover_engagement_opportunities()


def discover_engagement_opportunities_from_profile(external_id, provider_type):
  if provider_type == constants.Provider.TWITTER:
    twitter_engagement_discovery_provider.discover_engagement_opportunities_from_profile(external_id)
