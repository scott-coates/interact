NAME = 'name'
URL = 'url'
TEXT = 'text'
WEBSITES = 'websites'
LOCATION = 'location'
BIO = 'bio'
PROFILE_IDS = 'profile_ids'
EO_IDS = 'eo_ids'
PROSPECT_ID = 'prospect_id'
EO = 'engagement_opportunity'


class Profile:
  FOLLOWERS_COUNT = 'followers_count'
  FOLLOWING_COUNT = 'following_count'


class Provider:
  TWITTER = 'twitter'


class ProviderAction:
  TWITTER_TWEET = 'twitter_tweet'


class TopicOptionType:
  TWITTER_SEARCH = 'twitter_search'

# regarding enums, even without IntEnums they could be of value to us
# class Test(Enum):
#   twitter = 'twitter'
#
# >>> Test.twitter == Test.twitter
# True
