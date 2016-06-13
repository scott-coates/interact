import logging
from importlib import import_module

from src.domain.common import constants
from src.domain.common.constants import ProspectDict

logger = logging.getLogger(__name__)


def _get_rules_module(thing_to_score):
  rules_module = import_module("." + thing_to_score + "_rules_engine", __package__)
  return rules_module


def get_rules_engine_by_type_and_name(thing_to_score, provider_type=None):
  class_name = ProspectDict[thing_to_score]
  class_name += "RulesEngine"

  rules_module = _get_rules_module(thing_to_score)

  provider_name = ''
  if provider_type:
    provider_name = constants.ProviderDict[provider_type]

  class_name = "{0}{1}".format(provider_name, class_name)

  ret_val = getattr(rules_module, class_name)

  return ret_val
