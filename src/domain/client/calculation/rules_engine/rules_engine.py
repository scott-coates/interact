import logging

from src.domain.client.calculation.rules_engine import rules_engine_class_provider
from src.domain.common import constants

logger = logging.getLogger(__name__)

_assigned_entity_names = {
  constants.EO: "EngagementOpportunity",
  constants.PROFILE: "Profile",
}


class RulesEngine():
  def __init__(self, client_id):
    self.client_id = client_id

  def get_prospect_score(self, prospect, calc_data):
    rules_class = self._get_rules_engine_by_type_and_name(constants.PROSPECT)

    rules_instance = rules_class(prospect, calc_data)

    return rules_instance.score_it()

  def get_profile_score(self, profile, calc_data):
    rules_class = self._get_rules_engine_by_type_and_name(constants.PROFILE, profile.provider_type)

    rules_instance = rules_class(profile, calc_data)

    return rules_instance.score_it()

  def get_assigned_entity_score(self, assigned_entity_object, calc_data):
    rules_class = self._get_rules_engine_by_type_and_name(
        _assigned_entity_names[assigned_entity_object.entity_type], assigned_entity_object.provider_type
    )

    rules_instance = rules_class(assigned_entity_object.assigned_entity, calc_data)

    return rules_instance.score_it()

  def _get_rules_engine_by_type_and_name(self, thing_to_score, provider_type=None):
    rules_class = rules_engine_class_provider.get_rules_engine_by_type_and_name(
        thing_to_score, provider_type
    )

    return rules_class
