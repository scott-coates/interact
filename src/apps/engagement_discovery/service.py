import logging
from src.apps.engagement_discovery.providers.twitter import twitter_engagement_discovery_provider

logger = logging.getLogger(__name__)


def discover_engagement_opportunities():
  twitter_engagement_discovery_provider.discover_engagement_opportunities()
