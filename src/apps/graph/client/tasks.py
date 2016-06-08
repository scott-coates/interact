import logging

from django_rq import job

from src.apps.graph.client import services

logger = logging.getLogger(__name__)


@job('high')
def create_client_in_graphdb_task(client_id):
  return services.create_client_in_graphdb(client_id)['id']

#
# @shared_task(bind=True, max_retries=3, default_retry_delay=180)
# def create_subtopic_in_graphdb_task(self, topic_id, subtopic_id):
#   try:
#     return services.create_subtopic_in_graphdb(topic_id, subtopic_id)['topic_id']
#   except Exception as e:
#     # this can happen in the admin screen. Example: we add a topic and then sub topics. The Sub-topic tasks runs
#     # before the main parent topic even runs. We should wait until the main topic runs, then re-do this task in that
#     # case.
#
#     ex = Exception(
#       "Error creating subtopic. topic_id: %s subtopic_id: %s" %
#       (topic_id, subtopic_id)
#     ).with_traceback(e.__traceback__)
#
#     logger.debug(ex, exc_info=True)
#     self.retry(exc=ex)
#
#
# @shared_task(bind=True, max_retries=3, default_retry_delay=180)
# def delete_topic_in_graphdb_task(self, topic_id):
#   try:
#     return services.delete_topic_in_graphdb(topic_id)
#   except Exception as e:
#     logger.debug(e, exc_info=True)
#     self.retry(exc=e)
#
#
# @shared_task(bind=True, max_retries=3, default_retry_delay=180)
# def remove_subtopic_in_graphdb_task(self, topic_id, subtopic_id):
#   try:
#     return services.delete_subtopic_in_graphdb(topic_id, subtopic_id)
#   except Exception as e:
#     logger.debug(e, exc_info=True)
#     self.retry(exc=e)
