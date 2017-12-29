import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from db_manager import execute_select
from nltk.corpus import movie_reviews
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from pprint import pprint

def use_vader(sentence):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(sentence)

    max = 0
    ret = ""
    for k in ss:
        if ss[k] > max:
            max = ss[k]
            ret = k
    return ret

def parse_format(words):
    words = word_tokenize(words)
    useful_words = [word for word in words if word not in stopwords.words("english")]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict



def make_sentiment():
    neg_reviews = []
    list_comments = execute_select('SELECT text FROM ratings where score <= 2.5 LIMIT 200')
    print('\nNEGATIVE CALC\n')
    print(len(list_comments))
    for ratetext in list_comments:
        neg_reviews.append((parse_format(ratetext[0]), "neg"))

    pos_reviews = []
    list_comments = execute_select('SELECT text FROM ratings where score >= 2.5 LIMIT 200')
    print('\nPOSITIVE CALC\n')
    print(len(list_comments))
    for ratetext in list_comments:
        pos_reviews.append((parse_format(ratetext[0]), "pos"))
    train_set = neg_reviews + pos_reviews
    return NaiveBayesClassifier.train(train_set)

