NAME = 'name'
SCREEN_NAME = 'screen_name'
NAMES = 'names'
URL = 'url'
COMPARATIVE_TEXT = 'comparative_text'
TEXT = 'text'
WEBSITES = 'websites'
MENTIONS = 'mentions'
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
ENGAGEMENT_ASSIGNMENT = 'engagement_assignment'
PROFANITY_FILTER_WORDS = 'profanity_filter_words'
CLIENT_ID = 'client_id'
ID = 'id'
EXTERNAL_ID = 'external_id'
ATTRS = 'attrs'
SCORE = 'score'
PROSPECT_SCORE = 'prospect_score'
PROFILE_SCORE = 'profile_score'
ASSIGNED_ENTITY_SCORE = 'assigned_entity_score'
SCORE_ATTRS = 'score_attrs'
ASSIGNED_ENTITIES = 'assigned_entities'
ASSIGNED_ENTITY_TYPE = 'assigned_entity_type'
FOLLOWERS_COUNT = 'followers_count'
FOLLOWING_COUNT = 'following_count'
IS_RETWEET = 'is_retweet'
RECENT_EOS = 'recent_eos'
SIMILAR_EOS = 'similar_eos'
TOPICS = 'topics'
TOPIC_ID = 'topic_id'

DATA = 'data'

RELEVANCE = 'relevance'

NEW_PROSPECT_SCORE = 'new_prospect_score'
BIO_AVOID_KEYWORD_SCORE = 'bio_avoid_keyword_score'
BIO_TOPIC_SCORE = 'bio_topic_score'
LOCATION_SCORE = 'location_score'
EO_TOPIC_SCORE = 'eo_topic_score'
EO_MENTION_SCORE = 'eo_mention_score'
EO_SPAM_SCORE = 'eo_spam_score'

PROVIDER_TYPE = 'provider_type'
PROVIDER_ACTION_TYPE = 'provider_action_type'


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
