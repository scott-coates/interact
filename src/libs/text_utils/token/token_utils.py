# import nltk
#
# snowball = nltk.SnowballStemmer('english')


def stemmify_snowball_string(string):
  tokens = tokenize_words(string)
  return " ".join([find_snowball_stem(token) for token in tokens])


def find_snowball_stem(token):
  token = token.lower()

  stem = snowball.stem(token)

  return stem


def tokenize_words(string):
  # http://www.nltk.org/book/ch03.html
  tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+(?:[-']\w+)*|'|[-.(]+|\S\w*")
  return tokenizer.tokenize(string.lower())
