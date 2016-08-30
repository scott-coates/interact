import math
from collections import Counter, defaultdict

from src.apps.read_model.key_value.client.service import get_client_recent_engagement_assignment_scores
from src.apps.read_model.relational.client.service import get_prospect_ea_lookup, \
  get_profile_ea_lookups_by_prospect_id, \
  get_eo_ea_lookup
from src.domain.client.calculation.calculation_objects import AssignedEntity
from src.domain.client.calculation.rules_engine import rules_data_provider
from src.domain.client.calculation.rules_engine.rules_engine import RulesEngine
from src.domain.client.calculation.score_calculator import ScoreCalculator
from src.domain.common import constants

_binary_score_keys = (constants.LOCATION, constants.NEW_PROSPECT)


def get_engagement_assignment_score_attrs(client_id, assignment_attrs, _rules_data_provider=None):
  if not _rules_data_provider: _rules_data_provider = rules_data_provider

  score_attrs = {}

  assigned_calc_objects = _get_assigned_calc_objects(assignment_attrs)

  prospect_id = assigned_calc_objects[0].prospect_id
  prospect = get_prospect_ea_lookup(prospect_id)

  rules_data = _rules_data_provider.provide_rules_data(client_id, prospect_id)

  profiles = _get_profiles(assigned_calc_objects, prospect_id)

  rules_engine = RulesEngine(client_id)

  p_score_attrs = rules_engine.get_prospect_score(prospect, rules_data)
  score_attrs[constants.PROSPECT] = {
    constants.SCORE_ATTRS: p_score_attrs,
    constants.ID: prospect.id
  }

  score_attrs[constants.PROFILES] = {constants.DATA: []}
  for profile in profiles:
    p_score_attrs = rules_engine.get_profile_score(profile, rules_data)
    score_attrs[constants.PROFILES][constants.DATA].append({
      constants.SCORE_ATTRS: p_score_attrs,
      constants.ID: profile.id
    })

  score_attrs[constants.ASSIGNED_ENTITIES] = {constants.DATA: []}
  for ae in assigned_calc_objects:
    ae_score_attrs = rules_engine.get_assigned_entity_score(ae, rules_data)
    score_attrs[constants.ASSIGNED_ENTITIES][constants.DATA].append({
      constants.SCORE_ATTRS: ae_score_attrs,
      constants.ID: ae.assigned_entity_id,
      constants.ASSIGNED_ENTITY_TYPE: ae.assigned_entity_type
    })

  return score_attrs


def populate_batch_ea_scores(client_id, score_attrs):
  # todo client rule providers do they go here too?
  for score_attr in score_attrs:
    counter = Counter()

    prospect = score_attr[constants.PROSPECT]
    _increment_counter(prospect[constants.SCORE_ATTRS], counter)

    # putting profiles and AE's in a key called DATA because we might want other sibling keys like "length" in future.
    profiles = score_attr[constants.PROFILES][constants.DATA]
    for profile in profiles:
      _increment_counter(profile[constants.SCORE_ATTRS], counter)

    aes = score_attr[constants.ASSIGNED_ENTITIES][constants.DATA]
    for ae in aes:
      _increment_counter(ae[constants.SCORE_ATTRS], counter)

    counter_dict = {k: {constants.COUNT: v} for k, v in counter.items()}
    score_attr[constants.SCORE] = {constants.SCORE_ATTRS: counter_dict}

  tally = defaultdict(list)

  for score_attr in score_attrs:
    score_count_attrs = score_attr[constants.SCORE][constants.SCORE_ATTRS]
    _tally_counts(score_count_attrs, tally)

  recent_scores = get_client_recent_engagement_assignment_scores(client_id)
  for recent_score in recent_scores:
    _tally_counts(recent_score, tally)

  calcs = {}
  for k, v in tally.items():
    calc = ScoreCalculator(v)
    calcs[k] = calc

  for score_attr in score_attrs:
    total_score = 0
    score_count_attrs = score_attr[constants.SCORE][constants.SCORE_ATTRS]

    for k, v in score_count_attrs.items():
      count = v[constants.COUNT]

      if k in _binary_score_keys:
        score = count
      else:
        score = calcs[k].calculate_normalized_score(count)

      if k == constants.LOCATION:
        score *= 2.5

      if k == constants.BIO_TOPIC:
        score *= 1.25

      elif k == constants.EO_SPAM:
        eo_topic_count = len(score_attr[constants.ASSIGNED_ENTITIES][constants.DATA])
        spam_ratio = count / eo_topic_count
        score = math.log(max(1 - spam_ratio, .01)) * 2

      elif k == constants.BIO_AVOID_KEYWORD:
        score *= -1.10

      score_attr[constants.SCORE][constants.SCORE_ATTRS][k][constants.SCORE] = score

      total_score += score

    score_attr[constants.SCORE][constants.DATA] = total_score


def _tally_counts(count_attrs, tally):
  for k, v in count_attrs.items():
    if k not in _binary_score_keys:
      tally[k].append(v[constants.COUNT])


def _increment_counter(score_attrs, counter):
  for k, v in score_attrs.items():

    # the contract here is that COUNT is guaranteed to exist, so we don't need to rely on v.get('count', 0)
    try:
      counter[k] += v[constants.COUNT][constants.DATA]
    except KeyError as e:
      raise Exception('is missing', k).with_traceback(e.__traceback__)


def _get_profiles(assigned_calc_objects, prospect_id):
  # we used to have logic where you could assign a profile so we had to
  # get all unique profiles except those that we're going to assign.
  # this logic might come back in the future so lets keep this func encapsulated.

  assigned_profiles = [
    ae.assigned_entity_id for ae in assigned_calc_objects
    if ae.assigned_entity_type == constants.PROFILE
    ]

  profiles = get_profile_ea_lookups_by_prospect_id(prospect_id).exclude(id__in=assigned_profiles)

  return profiles


def _get_assigned_calc_objects(assignment_attrs):
  """
  Convert the attrs into ea entities
  """

  assigned_entities = []
  for assignment_attr, assigned_entity_ids in assignment_attrs.items():

    for id in assigned_entity_ids:

      if assignment_attr == constants.EO_IDS:
        eo_ea_lookup = get_eo_ea_lookup(id)
        assigned_entity_attrs = eo_ea_lookup.eo_attrs
        topic_ids = eo_ea_lookup.topic_ids
        provider_type = eo_ea_lookup.provider_type
        prospect_id = eo_ea_lookup.prospect_id
        entity_type = constants.EO
      else:
        raise ValueError("Invalid assignment attrs")

      assigned_entities.append(
          AssignedEntity(assigned_entity_attrs, id, entity_type, provider_type, prospect_id, topic_ids)
      )

  return assigned_entities
