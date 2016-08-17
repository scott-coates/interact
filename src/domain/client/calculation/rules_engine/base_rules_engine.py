import logging
from abc import ABC
from collections import Counter

from src.domain.common import constants
from src.libs.python_utils.objects.dict_utils import recursive_defaultdict

logger = logging.getLogger(__name__)


class BaseRulesEngine(ABC):
  def __init__(self):
    self.DEFAULT_COUNT_VALUE = 1

  def _get_default_score_attr_items(self):
    score_attrs, counter = recursive_defaultdict(), Counter()
    return score_attrs, counter

  def _set_score_attrs_value(self, score_attrs, key, value):
    score_attrs[key][constants.COUNT][constants.DATA] = value

  def _set_score_attrs_meta(self, score_attrs, key, meta_key, value):
    score_attrs[key][constants.SCORE_ATTRS][meta_key] = value
