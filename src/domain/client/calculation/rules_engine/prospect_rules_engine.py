import logging

from src.apps.read_model.key_value.client.service import get_client_assigned_prospect_count
from src.domain.client.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.domain.common import constants
from src.libs.geo_utils.services.geo_distance_service import mi_distance
from src.libs.text_utils.token import token_utils

logger = logging.getLogger(__name__)


class ProspectRulesEngine(BaseRulesEngine):
  def __init__(self, prospect_id, prospect_attrs, prospect_topic_ids, rules_data, _token_utils=None):
    super().__init__()

    if not _token_utils: _token_utils = token_utils
    self._token_utils = _token_utils

    self.prospect_id = prospect_id
    self.prospect_attrs = prospect_attrs
    self.prospect_topic_ids = prospect_topic_ids

    self.rules_data = rules_data

  def get_score_attrs(self):
    score_attrs = self._get_score_attrs()

    return score_attrs

  def _get_score_attrs(self):
    score_attrs = {}

    location_score_attrs = self._get_location_score_attrs()
    score_attrs.update(location_score_attrs)

    bio_score_attrs = self._get_bio_score_attrs()
    score_attrs.update(bio_score_attrs)

    prospect_assignment_score_attrs = self._get_prospect_assignment_score_attrs()
    score_attrs.update(prospect_assignment_score_attrs)

    return score_attrs

  def _get_location_score_attrs(self):
    score_attrs, counter = self._get_default_score_attr_items()

    p_locations = self.prospect_attrs.get(constants.LOCATIONS)
    r_locations = self.rules_data.get(constants.LOCATIONS)

    if p_locations and r_locations:
      # iterate through all rules_locations
      # if there is any intersection within _default_location_threshold miles, award the score
      for p_loc in p_locations:
        dest = (p_loc[constants.LAT], p_loc[constants.LNG])
        if any(mi_distance((r_loc[constants.LAT], r_loc[constants.LNG]), dest) < 35 for r_loc in r_locations):
          counter[constants.LOCATION] += self.DEFAULT_COUNT_VALUE

          self._set_score_attrs_value(score_attrs, constants.LOCATION, counter[constants.LOCATION])

    return score_attrs

  def _get_bio_score_attrs(self):
    score_attrs, counter = self._get_default_score_attr_items()

    topics = self.rules_data.get(constants.TOPICS)
    if topics:

      for k, v in topics.items():
        topic_id = v[constants.ID]
        if topic_id in self.prospect_topic_ids:
          counter[constants.BIO_TOPIC] += v[constants.RELEVANCE]

          self._set_score_attrs_meta(score_attrs, constants.BIO_TOPIC, topic_id, {constants.NAME: k})
          self._set_score_attrs_value(score_attrs, constants.BIO_TOPIC, counter[constants.BIO_TOPIC])

    bios = self.prospect_attrs.get(constants.BIOS)

    if bios:
      bio = ' '.join(bios)

      bio_tokens = self._token_utils.tokenize_string(bio)

      avoid_words = self.rules_data.get(constants.PROFANITY_FILTER_WORDS)

      if avoid_words:
        # score_attrs[constants.BIO_AVOID_KEYWORD] the namespace is only created if COUNT is provided, that's the
        # contract
        found_avoid_names = []

        # iterate through bio tokens to be less inclusive and prevent false positives (consider the word 'mass')
        for b in bio_tokens:
          if b in avoid_words:
            counter[constants.BIO_AVOID_KEYWORD] += self.DEFAULT_COUNT_VALUE
            found_avoid_names.append(b)

            self._set_score_attrs_value(score_attrs, constants.BIO_AVOID_KEYWORD, counter[constants.BIO_AVOID_KEYWORD])

        if found_avoid_names:
          self._set_score_attrs_meta(score_attrs, constants.BIO_AVOID_KEYWORD, constants.NAMES, found_avoid_names)

    return score_attrs

  def _get_prospect_assignment_score_attrs(self):
    score_attrs, counter = self._get_default_score_attr_items()

    client_id = self.rules_data[constants.CLIENT_ID]
    prospect_id = self.prospect_id

    new_prospect_for_client = get_client_assigned_prospect_count(client_id, prospect_id)
    if not new_prospect_for_client:
      self._set_score_attrs_value(score_attrs, constants.NEW_PROSPECT, self.DEFAULT_COUNT_VALUE)

    return score_attrs
