import logging

from src.domain.client.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.domain.common import constants
from src.libs.geo_utils.services.geo_distance_service import mi_distance
from src.libs.text_utils.token import token_utils

logger = logging.getLogger(__name__)


class ProspectRulesEngine(BaseRulesEngine):
  def __init__(self, prospect_attrs, rules_data, _token_utils=None):

    if not _token_utils: _token_utils = token_utils

    self._token_utils = _token_utils

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

    # website_score, website_score_attrs = self._apply_website_score()
    # score += website_score
    # score_attrs.update(website_score_attrs)
    #
    # email_score, email_score_attrs = self._apply_email_score()
    # score += email_score
    # score_attrs.update(email_score_attrs)
    #
    # prospect_assignment_score, prospect_assignment_score_attrs = self._apply_prospect_assignment_score()
    # score += prospect_assignment_score
    # score_attrs.update(prospect_assignment_score_attrs)

    return score, score_attrs

  # region apply score logic

  def _apply_location_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    p_locations = self.prospect_attrs.get(constants.LOCATIONS)
    r_locations = self.rules_data.get(constants.LOCATIONS)

    if p_locations and r_locations:
      location_score = 1
      # iterate through all rules_locations
      # if there is any intersection within _default_location_threshold miles, award the score
      # todo location threshold
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

  def _apply_website_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    websites = self.prospect.prospect_attrs.get(constants.WEBSITES)

    important_websites = self._important_websites

    if important_websites:

      if websites:

        website_score = self._website_score

        for ws in important_websites:
          if any(domain in ws.lower() for domain in self._important_websites):
            score += website_score
            counter[constants.WEBSITES_SCORE] += website_score

        if counter[constants.WEBSITES_SCORE]:
          score_attrs[constants.WEBSITES_SCORE] = counter[constants.WEBSITES_SCORE]

    return score, score_attrs

  def _apply_email_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    email_addresses = self.prospect.prospect_attrs.get(constants.EMAIL_ADDRESSES)

    if email_addresses:
      score += self._email_score
      counter[constants.EMAIL_ADDRESSES_SCORE] += self._email_score

    if counter[constants.EMAIL_ADDRESSES_SCORE]:
      score_attrs[constants.EMAIL_ADDRESSES_SCORE] = counter[constants.EMAIL_ADDRESSES_SCORE]

    return score, score_attrs

  def _apply_prospect_assignment_score(self):
    score, score_attrs, counter = self._get_default_score_items()

    client_uid = self.rules_data[constants.CLIENT_UID]
    prospect_uid = self.prospect.prospect_uid

    try:
      self._assigned_prospect_service.get_assigned_prospect_from_attrs(client_uid, prospect_uid)
    except:
      new_prospect_score = self._new_prospect_score
      score += new_prospect_score
      score_attrs[constants.NEW_PROSPECT_SCORE] = new_prospect_score
      logger.debug("new assigned prospect. client_uid: %s prospect_uid: %s", client_uid, prospect_uid)
    else:
      logger.debug("existing assigned prospect. client_uid: %s prospect_uid: %s", client_uid, prospect_uid)

    return score, score_attrs

  # endregion apply score logic

  # region define prospect scoring attrs

  @property
  def _important_locations(self):
    return ()

  @property
  def _location_score(self):
    return 1

  @property
  def _important_home_countries(self):
    return ()

  @property
  def _age_range(self):
    return (None, None)

  @property
  def _age_score(self):
    return 1

  @property
  def _preferred_gender(self):
    return None

  @property
  def _gender_score(self):
    return 1

  @property
  def _important_bio_keywords(self):
    return ()

  @property
  def _bio_important_keyword_score(self):
    return 1

  @property
  def _bio_client_topic_score(self):
    return 1

  @property
  def _important_websites(self):
    return ()

  @property
  def _website_score(self):
    return 1

  @property
  def _email_score(self):
    return 1

  @property
  def _new_prospect_score(self):
    return 1

  @property
  def _bio_avoid_keywords(self):
    return ()

  @property
  def _bio_avoid_keyword_score(self):
    return -1

  "pycharm recognize region"
  # endregion define prospect scoring attrs
