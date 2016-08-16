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
    self.mdev = (1 / (len(self.counts) - 1)) * abs_data.sum()

    self.sdev = np.std(self.counts)

  def calculate_normalized_score(self, value):
    norm = (value - self.min) / self.max
    return norm

  def calculate_modified_standard_score(self, value):
    # modified standard score
    modified_standard_score = np.nan_to_num((value - self.median) / self.mdev)

    return modified_standard_score

  def calculate_standard_score(self, value):
    # standard score
    standard_score = np.nan_to_num((value - self.mean) / self.sdev)

    return standard_score
