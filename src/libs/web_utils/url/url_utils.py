import logging

logger = logging.getLogger(__name__)


def get_unique_urls_from_iterable(websites):
  return list(set(filter(bool, websites)))
