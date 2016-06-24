# http://stackoverflow.com/questions/16439301/cant-pickle-defaultdict
from collections import defaultdict


def l():
  return defaultdict(l)


recursive_defaultdict = l
