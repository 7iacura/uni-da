from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from db_manager import *
from random import *
from pprint import pprint
import gensim
from sentimentLDA import *
from sentiment import *

initialize_dataset()
import_json('food2.json')





