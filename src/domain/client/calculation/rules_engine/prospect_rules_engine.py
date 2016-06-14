import logging

from dateutil.relativedelta import relativedelta
from django.utils import timezone

from src.domain.client.calculation.rules_engine.base_rules_engine import BaseRulesEngine
from src.domain.common import constants
from src.libs.geo_utils.services.geo_distance_service import mi_distance
from src.libs.nlp_utils.services.enums import GenderEnum

logger = logging.getLogger(__name__)


class ProspectRulesEngine(BaseRulesEngine):
  def __init__(
      self, prospect_attrs, rules_data,
      _geo_location_service=None, _iter_utils=None, _assigned_prospect_service=None, _datetime_parser=None):

    self.prospect_attrs= prospect_attrs
    self.rules_data = rules_data

    # if not _geo_location_service: _geo_location_service = geo_location_service
    # self._geo_location_service = _geo_location_service
    #
    # if not _iter_utils: _iter_utils = iter_utils
    # self._iter_utils = _iter_utils
    #
    # if not _assigned_prospect_service: _assigned_prospect_service = assigned_prospect_service
    # self._assigned_prospect_service = _assigned_prospect_service
    #
    # if not _datetime_parser: _datetime_parser = datetime_parser
    # self._datetime_parser = _datetime_parser

  def score_it(self):
    score, score_attrs = self._apply_score()

    return score, score_attrs

  def _apply_score(self):
    score, score_attrs = 0, {}

    location_score, location_score_attrs = self._apply_location_score()
    score += location_score
    score_attrs.update(location_score_attrs)

    # bio_score, bio_score_attrs = self._apply_bio_score()
    # score += bio_score
    # score_attrs.update(bio_score_attrs)
    #
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
      # if there is any intersection within 35 miles, award the score
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
      bio = self._iter_utils.stemmify_string(bio)

      # region client_id topic
      client_topics = self.rules_data[constants.STEMMED_TA_TOPIC_KEYWORDS]
      if client_topics:
        bio_client_topic_score = self._bio_client_topic_score

        for stemmed_topic_keyword in client_topics:
          if stemmed_topic_keyword in bio:
            score += bio_client_topic_score
            counter[constants.BIO_CLIENT_TA_TOPIC_SCORE] += bio_client_topic_score

        if counter[constants.BIO_CLIENT_TA_TOPIC_SCORE]:
          score_attrs[constants.BIO_CLIENT_TA_TOPIC_SCORE] = counter[constants.BIO_CLIENT_TA_TOPIC_SCORE]

      "pycharm doesn't recognize endregion"
      # endregion client_id topic

      # region important keywords
      bio_keywords = self._important_bio_keywords

      if bio_keywords:
        bio_keywords = self._iter_utils.stemmify_iterable(bio_keywords)

        bio_score = self._bio_important_keyword_score

        for kw in bio_keywords:
          if kw in bio:
            score += bio_score
            counter[constants.BIO_IMPORTANT_KEYWORD_SCORE] += bio_score

        if counter[constants.BIO_IMPORTANT_KEYWORD_SCORE]:
          score_attrs[constants.BIO_IMPORTANT_KEYWORD_SCORE] = counter[constants.BIO_IMPORTANT_KEYWORD_SCORE]

      "pycharm doesn't recognize endregion"
      # endregion important keywords

      # region avoid keywords
      bio_keywords = self._important_bio_keywords

      if bio_keywords:
        bio_keywords = self._iter_utils.stemmify_iterable(bio_keywords)

        bio_score = self._bio_important_keyword_score

        avoid_words = self.rules_data[constants.PROFANITY_FILTER_WORDS]

        avoid_words += self._bio_avoid_keywords

        avoid_words = self._iter_utils.stemmify_iterable(avoid_words)

        for kw in bio_keywords:
          if kw in avoid_words:
            score += bio_score
            counter[constants.BIO_AVOID_KEYWORD_SCORE] += bio_score

        if counter[constants.BIO_AVOID_KEYWORD_SCORE]:
          score_attrs[constants.BIO_AVOID_KEYWORD_SCORE] = counter[constants.BIO_AVOID_KEYWORD_SCORE]

      "pycharm doesn't recognize endregion"
      # endregion avoid keywords

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
