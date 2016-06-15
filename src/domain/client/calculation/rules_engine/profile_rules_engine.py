import logging
from abc import abstractmethod

from src.domain.client.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.libs.python_utils.collections import iter_utils

logger = logging.getLogger(__name__)


class ProfileRulesEngine(BaseRulesEngine):
  def __init__(self, profile_id, profile_attrs, rules_data, _iter_utils=None):
    if not _iter_utils: _iter_utils = iter_utils
    self._iter_utils = _iter_utils

    self.profile_id = profile_id
    self.profile_attrs = profile_attrs

    self.rules_data = rules_data

  def score_it(self):
    score, score_attrs = self._apply_score()

    return score, score_attrs

  @abstractmethod
  def _apply_score(self):
    pass


class TwitterProfileRulesEngine(ProfileRulesEngine):
  def _apply_score(self):
    score, score_attrs = 0, {}

    return score, score_attrs
