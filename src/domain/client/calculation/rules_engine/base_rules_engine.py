import logging
from abc import ABC
from collections import Counter

from src.libs.python_utils.objects.dict_utils import recursive_defaultdict

logger = logging.getLogger(__name__)


class BaseRulesEngine(ABC):
  def _get_default_score_items(self):
    score, score_attrs, counter = 0, recursive_defaultdict(), Counter()
    return score, score_attrs, counter
