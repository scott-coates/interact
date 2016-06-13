from src.apps.relational.prospect.service import get_engagement_opportunity_lookup
from src.domain.client.calculation import score_processor, calculation_data_provider
from src.domain.common import constants


def _get_profiles(assigned_calc_objects, prospect):
  # get all unique profiles except those that we're going to assign

  assigned_profiles = [ae.id for ae in assigned_calc_objects if ae.entity_type == constants.PROFILE]

  profiles = prospect.profiles.exclude(id__in=assigned_profiles)

  return profiles


def calculate_engagement_assignment_score(client_id, assignment_attrs, _score_processor=None, _calc_data_provider=None):
  if not _score_processor: _score_processor = score_processor
  if not _calc_data_provider: _calc_data_provider = calculation_data_provider

  calc_data = _calc_data_provider.provide_calculation_data()

  score_attrs = {}

  rules_engine = RulesEngine(client_id)

  prospect_score_object = rules_engine.get_prospect_score(prospect, calc_data)
  score_attrs[constants.PROSPECT] = {
    constants.BASE_SCORE: prospect_score_object.base_score,
    constants.BASE_SCORE_ATTRS: prospect_score_object.base_score_attrs,
    constants.INTERNAL_SCORE: prospect_score_object.internal_score,
    constants.INTERNAL_SCORE_ATTRS: prospect_score_object.internal_score_attrs,
    constants.UID: prospect.prospect_uid
  }

  profiles = _get_profiles(assigned_calc_objects, prospect)

  score_attrs[constants.PROFILES] = []
  for profile in profiles:
    profile_score_object = rules_engine.get_profile_score(profile, calc_data)
    score_attrs[constants.PROFILES].append({
      constants.BASE_SCORE: profile_score_object.base_score,
      constants.BASE_SCORE_ATTRS: profile_score_object.base_score_attrs,
      constants.INTERNAL_SCORE: profile_score_object.internal_score,
      constants.INTERNAL_SCORE_ATTRS: profile_score_object.internal_score_attrs,
      constants.UID: profile.profile_uid,
      'provider_type': profile.provider_type,
    })

  # loop through ae's
  score_attrs[constants.ASSIGNED_ENTITIES] = []
  for ae in assigned_calc_objects:
    ae_score_object = rules_engine.get_assigned_entity_score(ae, calc_data)
    score_attrs[constants.ASSIGNED_ENTITIES].append({
      constants.BASE_SCORE: ae_score_object.base_score,
      constants.BASE_SCORE_ATTRS: ae_score_object.base_score_attrs,
      constants.INTERNAL_SCORE: ae_score_object.internal_score,
      constants.INTERNAL_SCORE_ATTRS: ae_score_object.internal_score_attrs,
      constants.UID: ae.assigned_entity_uid,
      constants.ENTITY_TYPE: ae.entity_type,
      constants.PROVIDER_TYPE: ae.provider_type
    })

  score, score_attrs = _score_processor.process_score(client_id, score_attrs)

  return score, score_attrs


def get_rules_engine(client):
  if client.client_type == ClientTypeEnum.saas_tech_startup:
    return SaaSTechStartupRulesEngine()
  elif client.client_type == ClientTypeEnum.marketing_tech_startup:
    return MarketingTechStartupRulesEngine()
  elif client.client_type == ClientTypeEnum.ya_author:
    return YAAuthorRulesEngine()
  elif client.client_type == ClientTypeEnum.video_convo_tech_startup:
    return VideoConvoTechStartupRulesEngine()
  elif client.client_type == ClientTypeEnum.professional_social_networking_tech_startup_rules_engine:
    return ProfessionalSocialNetworkingTechStartupRulesEngine()
  elif client.client_type == ClientTypeEnum.sports_meetup_tech_startup_rules_engine:
    return SportsMeetupTechStartupRulesEngine()
  elif client.client_type == ClientTypeEnum.appointment_finding_tech_startup_affiliate_rules_engine:
    return AppointmentFindingTechStartupAffiliateRulesEngine()
  elif client.client_type == ClientTypeEnum.appointment_finding_tech_startup_client_rules_engine:
    return AppointmentFindingTechStartupClientRulesEngine()
  elif client.client_type == ClientTypeEnum.ya_writing_meetup_rules_engine:
    return YAWritingMeetupRulesEngine()
  elif client.client_type == ClientTypeEnum.food_lover_startup_rules_engine:
    return FoodLoverTechStartupRulesEngine()

  raise ValueError("No rules exist for this client")


def _get_assigned_calc_objects(assignment_attrs):
  """
  Convert the attrs into ea entities
  """

  assigned_entities = []
  for assignment_attr, assigned_entity_ids in assignment_attrs.items():

    for id in assigned_entity_ids:

      if assignment_attr == constants.EO_IDS:
        assigned_entity = get_engagement_opportunity_lookup(id)
        provider_type = assigned_entity.provider_type
        entity_type = constants.EO
      else:
        raise ValueError("Invalid assignment attrs")

      assigned_entities.append(
          CalculationAssignedEntityObject(assigned_entity, assigned_entity.id, entity_type, provider_type)
      )

  return assigned_entities
