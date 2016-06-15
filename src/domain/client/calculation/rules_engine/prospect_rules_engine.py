import logging

from src.apps.key_value.client.service import client_contains_assigned_prospect
from src.domain.client.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.domain.common import constants
from src.libs.geo_utils.services.geo_distance_service import mi_distance
from src.libs.text_utils.token import token_utils

logger = logging.getLogger(__name__)


class ProspectRulesEngine(BaseRulesEngine):
  def __init__(self, prospect_id, prospect_attrs, rules_data, _token_utils=None):

    if not _token_utils: _token_utils = token_utils
    self._token_utils = _token_utils

    self.prospect_id = prospect_id
    self.prospect_attrs = prospect_attrs

    self.rules_data = rules_data

  def score_it(self):
    score, score_attrs = self._apply_score()

    return score, score_attrs

  def _apply_score(self):
    score, score_attrs = 0, {}

    location_score, location_score_attrs = self._apply_location_score()
    score += location_score
    score_attrs.update(location_score_attrs)

    bio_score, bio_score_attrs = self._apply_bio_score()
    score += bio_score
    score_attrs.update(bio_score_attrs)

    prospect_assignment_score, prospect_assignment_score_attrs = self._apply_prospect_assignment_score()
    score += prospect_assignment_score
    score_attrs.update(prospect_assignment_score_attrs)

    return score, score_attrs

  def _apply_location_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    p_locations = self.prospect_attrs.get(constants.LOCATIONS)
    r_locations = self.rules_data.get(constants.LOCATIONS)

    if p_locations and r_locations:
      location_score = 1
      # iterate through all rules_locations
      # if there is any intersection within _default_location_threshold miles, award the score
      for p_loc in p_locations:
        dest = (p_loc[constants.LAT], p_loc[constants.LNG])
        if any(mi_distance((r_loc[constants.LAT], r_loc[constants.LNG]), dest) < 35 for r_loc in r_locations):
          score += location_score
          counter[constants.LOCATION_SCORE] += location_score

      if counter[constants.LOCATION_SCORE]: score_attrs[constants.LOCATION_SCORE] = counter[constants.LOCATION_SCORE]

    return score, score_attrs

  def _apply_bio_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    bios = self.prospect_attrs.get(constants.BIOS)

    if bios:
      bio = self._token_utils.stemmify_snowball_string(' '.join(bios))

      keywords = self.rules_data.get(constants.KEYWORDS)
      if keywords:
        bio_keyword_score = 1
        for k in keywords:
          if k in bio:
            score += bio_keyword_score
            counter[constants.BIO_KEYWORD_SCORE] += bio_keyword_score

        if counter[constants.BIO_KEYWORD_SCORE]:
          score_attrs[constants.BIO_KEYWORD_SCORE] = counter[constants.BIO_KEYWORD_SCORE]

      avoid_words = self.rules_data.get(constants.PROFANITY_FILTER_WORDS)
      if avoid_words:
        bio_avoid_keyword_score = -1
        for aw in avoid_words:
          if aw in bio:
            score += bio_avoid_keyword_score
            counter[constants.BIO_AVOID_KEYWORD_SCORE] += bio_avoid_keyword_score

        if counter[constants.BIO_AVOID_KEYWORD_SCORE]:
          score_attrs[constants.BIO_AVOID_KEYWORD_SCORE] = counter[constants.BIO_AVOID_KEYWORD_SCORE]

    return score, score_attrs

  def _apply_prospect_assignment_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    client_id = self.rules_data[constants.CLIENT_ID]
    prospect_id = self.prospect_id

    new_prospect_for_client = client_contains_assigned_prospect(client_id, prospect_id)
    if not new_prospect_for_client:
      new_prospect_score = 1
      score += new_prospect_score
      score_attrs[constants.NEW_PROSPECT_SCORE] = new_prospect_score

    return score, score_attrs
