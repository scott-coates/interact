from src.apps.engagement_discovery.providers.twitter.tasks import \
  discover_engagement_opportunities_from_twitter_ta_topics_task


def discover_engagement_opportunities():
  # Find all keywords that are ready to be ran
  # Iterate through keywords and kick async task to do twitter searches
  # Hand off to twitter service to analyze tweets and filter
  # Hand off remaining tweets to core library to analyze and filter

  discover_engagement_opportunities_from_twitter_ta_topics_task.delay()
