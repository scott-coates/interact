import datetime

from dateutil.relativedelta import relativedelta

from src.libs.social_utils.providers.twitter import twitter_client_provider
# http://stackoverflow.com/questions/13643823/exclude-replies-from-official-twitter-search-widget
# http://stackoverflow.com/questions/27941940/how-to-exclude-retweets-and-replies-in-a-search-api
from src.libs.social_utils.providers.twitter.signals import twitter_searched

_EXCLUDE_RT = 'exclude:retweets'
_EXCLUDE_RP = 'exclude:replies'


def get_time_period_back(since):
  since = since.lower()

  if since == "y":
    relative_delta = {"years": 1}
  elif since == "q":
    relative_delta = {"months": 3}
  elif since == "m":
    relative_delta = {"months": 1}
  elif since == "w":
    relative_delta = {"weeks": 1}
  elif since == "d":
    relative_delta = {"days": 1}
  else:
    raise ValueError("invalid since value")

  since_date_range = (datetime.datetime.utcnow() - relativedelta(**relative_delta)).strftime("%Y-%m-%d")

  return since_date_range


def search_twitter_by_user(screen_name,
                           since=None,
                           lang="en",
                           count=100, _twitter_client_provider=twitter_client_provider):
  client = _twitter_client_provider.get_twitter_client()

  search_params = {"lang": lang, "count": count}

  search_params["screen_name"] = screen_name

  if since:
    search_params["since"] = get_time_period_back(since)

  ret_val = client.get_user_timeline(**search_params)

  twitter_searched.send(None)

  return ret_val


def search_twitter(query,
                   screen_name=None,
                   geocode=None,
                   exclude_retweets=False, exclude_replies=False, since=None,
                   lang="en", include_entities=False, count=100, result_type='recent',
                   _twitter_client_provider=twitter_client_provider):
  client = _twitter_client_provider.get_twitter_client()

  search_params = {"lang": lang, "include_entities": include_entities, "count": count, "result_type": result_type}

  if exclude_retweets:
    query = "{0} {1}".format(_EXCLUDE_RT, query)

  if exclude_replies:
    query = "{0} {1}".format(_EXCLUDE_RP, query)

  if screen_name:
    search_params["from"] = screen_name

  if geocode:
    search_params["geocode"] = geocode

  search_params["q"] = query

  if since:
    search_params["since"] = get_time_period_back(since)

  ret_val = client.search(**search_params)

  twitter_searched.send(None)

  return ret_val
