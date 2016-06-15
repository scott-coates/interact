from src.domain.common import constants


def process_score(score_attrs):
  score = score_attrs[constants.PROSPECT][constants.SCORE] + \
          sum([x[constants.SCORE] for x in score_attrs[constants.PROFILES]]) + \
          sum([x[constants.SCORE] for x in score_attrs[constants.ASSIGNED_ENTITIES]])

  return score, score_attrs
