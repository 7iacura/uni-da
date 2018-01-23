import sys
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer


class Document_Parser():

	def __init__(self):
		# initialize tokenizer
		self.tokenizer = RegexpTokenizer(r'\w+')

		# create English stop words list
		self.en_stop = get_stop_words('en')
		self.en_stop.append('<br>')
		self.en_stop.append('br')

		# Create p_stemmer of class PorterStemmer
		self.p_stemmer = PorterStemmer()

	def add_to_stop(self, word):
		self.en_stop.append(word)

	def parse(self, document):
		# print(document)
		raw = document.lower()
		tokens = self.tokenizer.tokenize(raw)
		# remove stop words from tokens
		stopped_tokens = [i for i in tokens if not i in self.en_stop]
		# stem token
		stemmed_tokens = [self.p_stemmer.stem(i) for i in stopped_tokens]
		# Convert to a set and back into a list.
		stemmed_tokens_set = set(stemmed_tokens)
		stemmed_tokens_without_duplicated = list(stemmed_tokens_set)
		# print(stemmed_tokens_without_duplicated, '\n')

		return stemmed_tokens_without_duplicated


# # as demo,
# # decomment print lines,
# # and watch output in console
# doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother. <br>"
# doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
# doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
# doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
# doc_e = "Health professionals say that brocolli is good for your health."
# doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]
#
# # create class Document_Parser()
# parser = Document_Parser()
# # loop on documents
# for doc in doc_set:
# 	parser.parse(doc)

