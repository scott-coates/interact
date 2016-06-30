import logging

from django_rq import job

from src.apps.engagement_discovery.providers.twitter.service import \
  discover_engagement_opportunities_from_twitter_ta_topic_option
from src.apps.relational.client import service as client_service
from src.domain.common import constants

logger = logging.getLogger(__name__)


@job('default')
def discover_engagement_opportunities_task():
  # Find all keywords that are ready to be ran
  # Iterate through keywords and kick async task to do twitter searches
  # Hand off to twitter service to analyze tweets and filter
  # Hand off remaining tweets to core library to analyze and filter

  _discover_engagement_opportunities_from_twitter_ta_topics()


@job('default')
def discover_engagement_opportunities_from_profile_task(external_id):
  _discover_engagement_opportunities_from_twitter_ta_topics(_filter_ta_topic_by_relevance, screen_name=external_id)


@job('default')
def discover_engagement_opportunities_from_twitter_ta_topic_option_task(ta_topic_option_id, **kwargs):
  ta_topic_option = client_service.get_ta_topic_option(ta_topic_option_id)
  return discover_engagement_opportunities_from_twitter_ta_topic_option(ta_topic_option, **kwargs)


def _filter_ta_topic_by_relevance(ta_topic_option):
  ret_val = False
  rel = ta_topic_option.ta_topic_relevance
  if rel > 0:
    ret_val = True
    logger.debug('%s is accepted ', ta_topic_option)
  else:
    logger.debug('%s is rejected', ta_topic_option)

  return ret_val


def _discover_engagement_opportunities_from_twitter_ta_topics(filter_func=lambda _: True, **kwargs):
  discover = discover_engagement_opportunities_from_twitter_ta_topic_option_task

  ta_topic_options_to_run = client_service.get_active_ta_topic_options(). \
    filter(option_type=constants.TopicOptionType.TWITTER_SEARCH)

  for ta_topic_option in filter(filter_func, ta_topic_options_to_run):
    discover.delay(ta_topic_option.id, **kwargs)
