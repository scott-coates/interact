# https://gist.github.com/rochacbruno/2883505
# http://www.johndcook.com/blog/python_longitude_latitude/
import math

radius = 3960  # mi


# radius = 6371 # km
def mi_distance(origin, destination):
  lat1, lon1 = origin
  lat2, lon2 = destination

  dlat = math.radians(lat2 - lat1)
  dlon = math.radians(lon2 - lon1)
  a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
                                                * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  d = radius * c

  return d
