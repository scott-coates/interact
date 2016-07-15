from django.dispatch import receiver

from src.apps.key_value.social import service
from src.libs.social_utils.providers.twitter.signals import twitter_searched


@receiver(twitter_searched)
def handle_twitter_search(sender, **kwargs):
  # note: we're not calling a task/job here because in order for rate limiting to be effective, queueing the tasks
  # won't do much good if the rate limit counter is batched up
  service.record_twitter_search()
