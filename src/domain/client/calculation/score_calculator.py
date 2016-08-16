import numpy as np

from src.domain.common import constants


class ScoreCalculator:
  def __init__(self, scores):
    self.scores = scores

    # get median
    self.median = np.median(self.scores)

    # get mean
    self.mean = np.mean(self.scores)

    # normalize the median for each val in the list
    abs_data = np.abs(self.scores - self.median)

    # refer to guidetodatamining chapter 4 for abs standard devation
    # sample size = len(scores) - 1. chapter 6 guidetodatamining.
    # http://stackoverflow.com/a/16562028/173957
    self.mdev = (1 / (len(self.scores) - 1)) * abs_data.sum()

    self.sdev = np.std(self.scores)

  def calculate_score(self, score_attrs):
    parts = self._get_score_parts(score_attrs)

    prospect_score = parts[constants.PROSPECT]
    profile_score = parts[constants.PROFILES]
    ae_score = parts[constants.ASSIGNED_ENTITIES]

    # modified standard score
    prospect_new = np.nan_to_num((prospect_score - self.prospect_median) / self.prospect_mdev)
    profile_new = np.nan_to_num((profile_score - self.profile_median) / self.profile_mdev)
    ae_new = np.nan_to_num((ae_score - self.ae_median) / self.ae_mdev)

    # standard score
    prospect_new = np.nan_to_num((prospect_score - self.prospect_mean) / self.prospect_sdev)
    profile_new = np.nan_to_num((profile_score - self.profile_mean) / self.profile_sdev)
    ae_new = np.nan_to_num((ae_score - self.ae_mean) / self.ae_sdev)

    normalized_parts = {
      constants.PROSPECT: prospect_new,
      constants.PROFILES: profile_new,
      constants.ASSIGNED_ENTITIES: ae_new,
    }

    score = prospect_new + profile_new + ae_new

    return score, parts, normalized_parts

  def _get_score_parts(self, score_attrs):
    parts = {
      constants.PROSPECT: score_attrs[constants.PROSPECT][constants.SCORE],
      constants.PROFILES: sum([x[constants.SCORE] for x in score_attrs[constants.PROFILES][constants.DATA]]),
      constants.ASSIGNED_ENTITIES: sum([x[constants.SCORE] for x in score_attrs[constants.ASSIGNED_ENTITIES][
        constants.DATA]])
    }

    return parts
