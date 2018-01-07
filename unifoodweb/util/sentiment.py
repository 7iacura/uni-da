import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from db_manager import execute_select,execute_statement
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
		if (k != 'compound'):
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
	list_comments = execute_select('SELECT text FROM rating where score <= 2')
	print('\nNEGATIVE CALC\n')
	print(len(list_comments))
	for ratetext in list_comments:
		neg_reviews.append((parse_format(ratetext[0]), "neg"))

	pos_reviews = []
	list_comments = execute_select('SELECT text FROM rating where score >= 4')
	print('\nPOSITIVE CALC\n')
	print(len(list_comments))
	for ratetext in list_comments:
		pos_reviews.append((parse_format(ratetext[0]), "pos"))

	neut_reviews = []
	list_comments = execute_select('SELECT text FROM rating where score = 3')
	print('\nNEUTRAL CALC\n')
	print(len(list_comments))
	for ratetext in list_comments:
		neut_reviews.append((parse_format(ratetext[0]), "neut"))




	train_set = neg_reviews + pos_reviews + neut_reviews
	return NaiveBayesClassifier.train(train_set)

def analyze(classifier,text,userid,productid):
	naive = classifier.classify(parse_format(text))
	vader = use_vader(text)
	user = execute_select('select experience_level from user where id = "' + userid + '"')
	product = execute_select('select product_level from product where id = "' + productid + '"')
	if product[0][0] != None:
		if product[0][0] >= user[0][0] - 1 and product[0][0] >= user[0][0] - 1:
			response = 'positive'
		else:
			response = 'negative'






def update_experience(users,value):

	for user in users.split(','):
		execute_statement('update user set experience = experience + '+ str(value) + ' where id = "' + user+'"')



def calculate_user_experience():
	products = execute_select('select id from product')
	inc = 0
	for product in products:
		inc = inc +1
		print(inc)
		select = "select group_concat(userid),count(score) as num_score from rating where productid = '"+product[0]+"' group by score order by num_score desc"
		rat = execute_select(select)
		value = 1
		tmp = 0
		rate = 1/len(rat)
		for r in rat:
			if tmp != 0 and r[1] != tmp:
				value = value - rate
			tmp = r[1]
			update_experience(r[0],value)

def setlevel():
	execute_statement('update user set experience_level = 5 where experience > 23')
	execute_statement('update user set experience_level = 4 where experience > 15 and experience <= 23')
	execute_statement('update user set experience_level = 3 where experience >=5 and experience<=15')
	execute_statement('update user set experience_level = 2 where experience >=1 and experience < 5')
	execute_statement('update user set experience_level = 1 where experience <= 1')

def product_level():
	products = execute_select('select id from product where av_score > 3')
	for product in products:
		ret =execute_select('select max(max_exp),experience_level from(select productid,experience_level,count(experience_level) as max_exp,group_concat(score) from rating r,user u where u.id = r.userid  and productid = "' + product[0] + '" group by experience_level)')
		if ret[0][1] != None:
			execute_statement('update product set product_level = ' + str(ret[0][1])+ ' where id = "' + product[0] + '"')


