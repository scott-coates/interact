# todo why does importing nltk cause http and network requests to hang during rq tasks?
import nltk

# http://stackoverflow.com/questions/13965823/resource-corpora-wordnet-not-found-on-heroku
nltk.data.path.append('./src/nltk_data')
