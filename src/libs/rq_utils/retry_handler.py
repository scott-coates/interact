import logging
from datetime import timedelta

import django_rq

MAX_FAILURES = 3
RETRY_DELAYS = 5 * 60

FAILURES_KEY = 'failures'
logger = logging.getLogger(__name__)


# https://gist.github.com/spjwebster/6521272
def retry_handler(job, exc_type, exc_value, traceback):
  job.meta.setdefault(FAILURES_KEY, 0)
  failures_count = job.meta[FAILURES_KEY]
  failures_count += 1

  # Too many failures
  if failures_count >= MAX_FAILURES:
    job.save()

    logger.warn('job %s: failed too many times times - moving to failed queue' % job.id)

    ret_val = True
  else:
    # Requeue job and stop it from being moved into the failed queue
    scheduler = django_rq.get_scheduler(job.origin)

    scheduled_job = scheduler.enqueue_in(timedelta(seconds=RETRY_DELAYS), job.func, *job.args, **job.kwargs)
    scheduled_job.meta[FAILURES_KEY] = failures_count
    scheduled_job.save()

    # remove the old job from the queue
    job.delete()

    logger.warn('job %s: failed %d times - retrying' % (job.id, failures_count))

    ret_val = False

  return ret_val
