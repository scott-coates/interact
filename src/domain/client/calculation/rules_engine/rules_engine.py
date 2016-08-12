import logging

from src.domain.client.calculation.rules_engine import rules_engine_class_provider
from src.domain.common import constants

logger = logging.getLogger(__name__)


class RulesEngine():
  def __init__(self, client_id):
    self.client_id = client_id

  def get_prospect_score(self, prospect, rules_data):
    rules_class = self._get_rules_engine_by_type_and_name(constants.PROSPECT)

    rules_instance = rules_class(prospect.id, prospect.attrs, prospect.topic_ids, rules_data)

    return rules_instance.score_it()

  def get_profile_score(self, profile, rules_data):
    rules_class = self._get_rules_engine_by_type_and_name(constants.PROFILE, profile.provider_type)

    rules_instance = rules_class(profile.id, profile.profile_attrs, rules_data)

    return rules_instance.score_it()

  def get_assigned_entity_score(self, assigned_entity_object, rules_data):
    rules_class = self._get_rules_engine_by_type_and_name(
        assigned_entity_object.assigned_entity_type, assigned_entity_object.provider_type
    )

    rules_instance = rules_class(assigned_entity_object.assigned_entity_id,
                                 assigned_entity_object.assigned_entity_attrs,
                                 assigned_entity_object.topic_ids,
                                 assigned_entity_object.prospect_id,
                                 rules_data)

    return rules_instance.score_it()

  def _get_rules_engine_by_type_and_name(self, thing_to_score, provider_type=None):
    rules_class = rules_engine_class_provider.get_rules_engine_by_type_and_name(
        thing_to_score, provider_type
    )

    return rules_class
