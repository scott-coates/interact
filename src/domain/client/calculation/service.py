from collections import Counter, defaultdict

from src.apps.read_model.relational.client.service import get_prospect_ea_lookup, \
  get_profile_ea_lookups_by_prospect_id, \
  get_eo_ea_lookup, get_client_ea_lookup
from src.domain.client.calculation.calculation_objects import AssignedEntity
from src.domain.client.calculation.rules_engine import rules_data_provider
from src.domain.client.calculation.rules_engine.rules_engine import RulesEngine
from src.domain.client.calculation.score_calculator import ScoreCalculator
from src.domain.common import constants


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
  client = get_client_ea_lookup(client_id)

  topics = client.ta_topics.items()

  # todo rename to get_score_attrs_counts
  for score_attr in score_attrs:
    counter = Counter()

    prospect = score_attr[constants.PROSPECT]
    _increment_counter(prospect[constants.SCORE_ATTRS], counter)

    profiles = score_attr[constants.PROFILES][constants.DATA]
    for profile in profiles:
      _increment_counter(profile[constants.SCORE_ATTRS], counter)

    aes = score_attr[constants.ASSIGNED_ENTITIES][constants.DATA]  # todo remove constants.DATA??
    for ae in aes:
      _increment_counter(ae[constants.SCORE_ATTRS], counter)

    counter_dict = {k: {constants.COUNT: v} for k, v in counter.items()}
    score_attr[constants.SCORE] = {constants.SCORE_ATTRS: counter_dict}

  tally = defaultdict(list)

  for score_attr in score_attrs:
    count = score_attr[constants.SCORE][constants.SCORE_ATTRS]
    for k, v in count.items():
      tally[k].append(v[constants.COUNT])

  calcs = {}
  for k, v in tally.items():
    calc = ScoreCalculator(v)
    calcs[k] = calc

  for score_attr in score_attrs:
    total_score = 0
    count = score_attr[constants.SCORE][constants.SCORE_ATTRS]

    for k, v in count.items():
      score = calcs[k].calculate_normalized_score(v[constants.COUNT])

      if k == constants.BIO_TOPIC:
        score *= 2
      elif k == constants.EO_TOPIC:
        score *= 1.15
      elif k == constants.EO_SPAM:
        score *= -10
      elif k == constants.BIO_AVOID_KEYWORD:
        score *= -5

      score_attr[constants.SCORE][constants.SCORE_ATTRS][k][constants.DATA] = score

      total_score += score

    print('score: ', total_score)


def _increment_counter(score_attrs, counter):
  for k, v in score_attrs.items():

    # the contract here is that COUNT will exist so long as the key exists, so we don't need to rely on
    # v.get('count', 0)
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
