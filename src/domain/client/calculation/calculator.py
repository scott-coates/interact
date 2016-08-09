import numpy as np

from src.domain.common import constants


class ScoreCalculator:
  def __init__(self, score_attrs_col):
    self.prospect_scores = []
    self.profile_scores = []
    self.ae_scores = []

    for s in score_attrs_col:
      parts = self._get_score_parts(s)
      self.prospect_scores.append(parts[constants.PROSPECT])
      self.profile_scores.append(parts[constants.PROFILES])
      self.ae_scores.append(parts[constants.ASSIGNED_ENTITIES])

    # get median
    self.prospect_median = np.median(self.prospect_scores)
    self.profile_median = np.median(self.profile_scores)
    self.ae_median = np.median(self.ae_scores)

    # normalize the median for each val in the list
    prospect_abs_data = np.abs(self.prospect_scores - self.prospect_median)
    profile_abs_data = np.abs(self.profile_scores - self.profile_median)
    ae_abs_data = np.abs(self.ae_scores - self.ae_median)

    # refer to guidetodatamining chapter 4 for abs standard devation
    # sample size = len(scores) - 1. chapter 6 guidetodatamining.
    # http://stackoverflow.com/a/16562028/173957
    self.prospect_mdev = (1 / (len(self.prospect_scores) - 1)) * prospect_abs_data.sum()
    self.profile_mdev = (1 / (len(self.profile_scores) - 1)) * profile_abs_data.sum()
    self.ae_mdev = (1 / (len(self.ae_scores) - 1)) * ae_abs_data.sum()

  def calculate_score(self, score_attrs):
    parts = self._get_score_parts(score_attrs)

    prospect_score = parts[constants.PROSPECT]
    profiles_score = parts[constants.PROFILES]
    ae_score = parts[constants.ASSIGNED_ENTITIES]

    prospect_new = np.nan_to_num((prospect_score - self.prospect_median) / self.prospect_mdev)
    profile_new = np.nan_to_num((profiles_score - self.profile_median) / self.profile_mdev)
    ae_new = np.nan_to_num((ae_score - self.ae_median) / self.ae_mdev)

    score = prospect_new + profile_new + ae_new

    return score

  def _get_score_parts(self, score_attrs):
    parts = {
      constants.PROSPECT: score_attrs[constants.PROSPECT][constants.SCORE],
      constants.PROFILES: sum([x[constants.SCORE] for x in score_attrs[constants.PROFILES]]),
      constants.ASSIGNED_ENTITIES: sum([x[constants.SCORE] for x in score_attrs[constants.ASSIGNED_ENTITIES]])
    }

    return parts
