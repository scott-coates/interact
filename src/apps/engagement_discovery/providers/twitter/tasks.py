import logging

from django.conf import settings
from django_rq import job

from src.apps.engagement_discovery.providers.twitter.services import \
  discover_engagement_opportunities_from_twitter_ta_topic_option
from src.domain.topic import services as topic_service

logger = logging.getLogger(__name__)
constants = settings.constants


@job('default')
def discover_engagement_opportunities_from_twitter_ta_topics_task(**kwargs):
  discover = discover_engagement_opportunities_from_twitter_ta_topic_option_task

  ta_topics_to_run = topic_service.get_active_ta_topics()

  for ta_topic in ta_topics_to_run:
    for ta_topic_option in ta_topic.options:
      if ta_topic_option[constants.OPTION_TYPE] == constants.TWITTER_SEARCH:
        discover.delay(ta_topic_option.id, kwargs)


@job('default')
def discover_engagement_opportunities_from_twitter_ta_topic_option_task(ta_topic_option_id, **kwargs):
  ta_topic_option = topic_service.get_ta_topic_option(ta_topic_option_id)
  return discover_engagement_opportunities_from_twitter_ta_topic_option(ta_topic_option, **kwargs)
