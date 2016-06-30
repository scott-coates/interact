from src.apps.engagement_discovery.providers.twitter.tasks import \
  discover_engagement_opportunities_from_twitter_ta_topics_task


def discover_engagement_opportunities():
  # Find all keywords that are ready to be ran
  # Iterate through keywords and kick async task to do twitter searches
  # Hand off to twitter service to analyze tweets and filter
  # Hand off remaining tweets to core library to analyze and filter

  discover_engagement_opportunities_from_twitter_ta_topics_task.delay()


def discover_engagement_opportunities_from_profile(external_id):
  discover_engagement_opportunities_from_twitter_ta_topics_task.delay(_filter_ta_topic_by_relevance,
                                                                      screen_name=external_id)


def _filter_ta_topic_by_relevance(ta_topic_option):
  ret_val = False
  rel = ta_topic_option.ta_topic_relevance
  if rel > 0:
    ret_val = True

  return ret_val
