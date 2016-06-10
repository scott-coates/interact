URL = 'url'
TEXT = 'text'
WEBSITES = 'websites'


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
