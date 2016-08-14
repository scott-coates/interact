from nltk import TweetTokenizer
from nltk.corpus import stopwords as sp

from src.libs.text_utils.formatting.text_formatter import only_alpha_numeric
from src.libs.text_utils.token.token_utils import find_stem

invalid_tweet_token_prefix = ('http', '#', '@')
tt = TweetTokenizer()

stopwords = sp.words('english')


def get_comparative_text_from_tweet(tweet):
  text_tokens = tt.tokenize(tweet)

  comparative_text = filter(_valid_tweet_token_prefix, text_tokens)
  comparative_text = map(_normalize_tokens, comparative_text)
  comparative_text = (only_alpha_numeric(x).lower() for x in comparative_text)
  comparative_text = filter(_valid_tweet_token, comparative_text)
  comparative_text = list(filter(bool, comparative_text))

  return comparative_text


def _valid_tweet_token_prefix(token):
  ret_val = True

  if any(it for it in invalid_tweet_token_prefix if token.startswith(it)):
    ret_val = False

  return ret_val


def _valid_tweet_token(token):
  ret_val = True

  if token in stopwords:
    ret_val = False

  return ret_val


def _normalize_tokens(token):
  ret_val = find_stem(token)

  return ret_val
