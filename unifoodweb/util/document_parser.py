import sys
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer


def document_parser(document):

	tokenizer = RegexpTokenizer(r'\w+')

	raw = document.lower()
	tokens = tokenizer.tokenize(raw)
	# print(tokens)

	# create English stop words list
	en_stop = get_stop_words('en')

	# remove stop words from tokens
	stopped_tokens = [i for i in tokens if not i in en_stop]
	# print(stopped_tokens)

	# Create p_stemmer of class PorterStemmer
	p_stemmer = PorterStemmer()

	# stem token
	stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
	# print(stemmed_tokens)

	# Convert to a set and back into a list.
	stemmed_tokens_set = set(stemmed_tokens)
	stemmed_tokens_without_duplicated = list(stemmed_tokens_set)
	# print(stemmed_tokens_without_duplicated)
	# print('---')

	return stemmed_tokens_without_duplicated


# # as demo,
# # decomment print lines,
# # and watch output in console
# doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
# doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
# doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
# doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
# doc_e = "Health professionals say that brocolli is good for your health."
# doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]
# for doc in doc_set:
# 	document_parser(doc)
