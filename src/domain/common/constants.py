NAME = 'name'
NAMES = 'names'
URL = 'url'
TEXT = 'text'
WEBSITES = 'websites'
LOCATION = 'location'
LOCATIONS = 'locations'
LAT = 'lat'
LNG = 'lng'
BIO = 'bio'
BIOS = 'bios'
PROFILE_ID = 'profile_id'
PROFILE_IDS = 'profile_ids'
EO_IDS = 'eo_ids'
PROSPECT_ID = 'prospect_id'
EO = 'engagement_opportunity'
PROFILES = 'profiles'
PROFILE = 'profile'
PROSPECT = 'prospect'
PROFANITY_FILTER_WORDS = 'profanity_filter_words'
CLIENT_ID = 'client_id'
ID = 'id'
SCORE = 'score'
SCORE_ATTRS = 'score_attrs'
ASSIGNED_ENTITIES = 'assigned_entities'
ASSIGNED_ENTITY_TYPE = 'assigned_entity_type'
FOLLOWERS_COUNT = 'followers_count'
FOLLOWING_COUNT = 'following_count'

KEYWORDS = 'keywords'
TOPIC_KEYWORDS = 'topic_keywords'

SNOWBALL_STEM = 'snowball_stem'

NEW_PROSPECT_SCORE = 'new_prospect_score'
BIO_AVOID_KEYWORD_SCORE = 'bio_avoid_keyword_score'
BIO_KEYWORD_SCORE = 'bio_keyword_score'
LOCATION_SCORE = 'location_score'
EO_KEYWORD_SCORE = 'eo_keyword_score'


class Provider:
  TWITTER = 'twitter'


ProspectDict = {
  PROSPECT: "Prospect",
  PROFILE: "Profile",
  EO: "EngagementOpportunity",
}


class ProviderAction:
  TWITTER_TWEET = 'twitter_tweet'


ProviderDict = {Provider.TWITTER: 'Twitter'}


class TopicOptionType:
  TWITTER_SEARCH = 'twitter_search'


  # regarding enums, even without IntEnums they could be of value to us
  # class Test(Enum):
  #   twitter = 'twitter'
  #
  # >>> Test.twitter == Test.twitter
  # True
