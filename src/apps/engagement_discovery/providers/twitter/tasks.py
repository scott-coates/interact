import logging

from django_rq import job

from src.apps.engagement_discovery.providers.twitter.service import \
  discover_engagement_opportunities_from_twitter_ta_topic_option, discover_engagement_opportunities_from_twitter_user
from src.apps.relational.client import service as client_service
from src.domain.common import constants

logger = logging.getLogger(__name__)


@job('default')
def discover_engagement_opportunities_task():
  # Find all keywords that are ready to be ran
  # Iterate through keywords and kick async task to do twitter searches
  # Hand off to twitter service to analyze tweets and filter
  # Hand off remaining tweets to core library to analyze and filter
  discover = discover_engagement_opportunities_from_twitter_ta_topic_option_task

  ta_topic_options_to_run = client_service.get_active_ta_topic_options(). \
    filter(option_type=constants.TopicOptionType.TWITTER_SEARCH)

  for ta_topic_option in ta_topic_options_to_run:
    discover.delay(ta_topic_option.id)


@job('default')
def discover_engagement_opportunities_from_twitter_ta_topic_option_task(ta_topic_option_id):
  ta_topic_option = client_service.get_ta_topic_option(ta_topic_option_id)
  return discover_engagement_opportunities_from_twitter_ta_topic_option(ta_topic_option)


@job('default')
def discover_engagement_opportunities_from_user_task(external_id):
  return discover_engagement_opportunities_from_twitter_user(external_id)
