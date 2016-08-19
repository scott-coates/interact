import numpy as np


class ScoreCalculator:
  def __init__(self, counts):
    self.counts = counts

    # get median
    self.median = np.median(self.counts)

    # get mean
    self.mean = np.mean(self.counts)

    # get max
    # refer to guidetodatamining chapter 4 for normalization - page 18
    self.min = float(min(self.counts))
    self.max = float(max(self.counts))

    # normalize the median for each val in the list
    abs_data = np.abs(self.counts - self.median)

    # refer to guidetodatamining chapter 4 for abs standard devation
    # sample size = len(scores) - 1. chapter 6 guidetodatamining.
    # http://stackoverflow.com/a/16562028/173957

    len_counts = len(self.counts)
    self.mdev = 0.0 if len_counts == 1 else (1 / (len_counts - 1)) * abs_data.sum()

    self.sdev = np.std(self.counts)

  def calculate_normalized_score(self, value):
    try:
      norm = (value - self.min) / self.max
    except ZeroDivisionError:
      norm = 0
    # I removed this logic and am explicitly placing it for specific keys in the calc service.
    # min and max and value are all the same
    # x = ScoreCalculator([1,1,1,1,1,1])
    # x.calculate_normalized_score(1)
    # 1.0
    # this is so an EA doesn't get a score of 0 on the first round.
    # if self.min == value == self.max:
    #   norm = 1
    return norm

  def calculate_modified_standard_score(self, value):
    # modified standard score
    modified_standard_score = np.nan_to_num((value - self.median) / self.mdev)

    return modified_standard_score

  def calculate_standard_score(self, value):
    # standard score
    standard_score = np.nan_to_num((value - self.mean) / self.sdev)

    return standard_score
