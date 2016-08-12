from nltk import TweetTokenizer

from src.libs.text_utils.formatting.text_formatter import only_alpha_numeric

invalid_tweet_tokens = ('http', '#', '@')
tt = TweetTokenizer()


def get_comparative_text_from_tweet(tweet):
  text_tokens = tt.tokenize(tweet)

  comparative_text = filter(_valid_tweet_token, text_tokens)
  comparative_text = [only_alpha_numeric(x).lower() for x in comparative_text]
  comparative_text = list(filter(bool, comparative_text))

  return comparative_text


def _valid_tweet_token(token):
  ret_val = True

  if any(it for it in invalid_tweet_tokens if token.startswith(it)):
    ret_val = False

  return ret_val
