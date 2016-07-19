from math import log

from src.domain.common import constants


def process_score(score_attrs):
  score = score_attrs[constants.PROSPECT][constants.SCORE] + \
          sum([x[constants.SCORE] for x in score_attrs[constants.PROFILES]]) + \
          sum([x[constants.SCORE] for x in score_attrs[constants.ASSIGNED_ENTITIES]])

  return score, score_attrs


def _get_score(score):
  try:
    ret_val = log(max(score, 1), 10)
  except Exception as e:
    raise Exception('Error', score).with_traceback(e.__traceback__)
  return ret_val
