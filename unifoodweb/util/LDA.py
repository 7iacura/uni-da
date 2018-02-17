import math

import gensim
from gensim import corpora, models

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from sqlite3 import *
from pprint import pprint

from db_manager import *
from document_parser import *


def ldaProduct(productId):
    response = execute_select('SELECT text FROM RATING where productid = "'+ productId + '"')
    num_topics = execute_select('SELECT count (0) from RATING where productid = "'+ productId+ '"')
    words = lda(response,math.ceil(num_topics[0][0]/2),10)
    join = ','.join(str(e) for e in words)
    execute_statement('UPDATE product set words = "' + join + '" where id = "'+productId+'"')



def ldaUser(userId):
    response = execute_select('SELECT text FROM RATING where score <= 3 and userid = "' + userId+'"')
    num_topics = execute_select('SELECT distinct(productid) FROM RATING where score <= 3 and userid = "' + userId+'"')
    if len(response) > 0:
        words = lda(response,len(num_topics),4)

        join = ','.join(str(e) for e in words)

        execute_statement('UPDATE user set neg_words = "' + join + '" where id = "' + userId + '"')

    response = execute_select('SELECT text FROM RATING where score > 3 and userid = "' + userId+'"')
    num_topics = execute_select('SELECT distinct(productid) FROM RATING where score > 3 and userid = "' + userId+'"')
    if len(response) > 0:
        words = lda(response,len(num_topics),4)
        join = ','.join(str(e) for e in words)
        execute_statement('UPDATE user set pos_words = "' + join + '" where id = "' + userId + '"')



def lda(doc_set,num_topics,num_words):
    texts = []

    # create class DocumentParser()
    parser = DocumentParser()
    # loop on documents
    for doc in doc_set:
        p = parser.parse(doc[0])
        # add tokens to list
        texts.append(p)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]

    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=2)
    words = []
    for i in range(num_topics):
        words.extend([t[0] for t in ldamodel.show_topic(i,num_words)])
    return list(set(words))