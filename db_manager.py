import sqlite3, csv, sys
from pprint import pprint

class ProgressBar():

	def __init__(self, blen, slen):
		self.bar_len = blen
		self.total = slen
		self.current = 0

	def step(self):
		self.current += 1
		current_len = int(round(self.bar_len * self.current / float(self.total)))
		perc = round(100.0 * self.current / float(self.total), 1)
		bar = '=' * current_len + '-' * (self.bar_len - current_len)
		sys.stdout.write('\r[%s] %s%s | %s / %s' % (bar, perc, '%', self.current, self.total))
		sys.stdout.flush()


def execute_select(select):
	db = sqlite3.connect('dataset/dataset.db')
	crs = db.cursor()
	crs.execute(select)
	result = crs.fetchall()
	db.close()
	return result


def initialize_dataset():
	# connect to database (or create it)
	db = sqlite3.connect('dataset/dataset.db')
	crs = db.cursor()

	print('DROP TABLEs rating, user, product')
	# clean db of dataset
	crs.execute('DROP TABLE IF EXISTS product')
	crs.execute('DROP TABLE IF EXISTS user')
	crs.execute('DROP TABLE IF EXISTS rating')
	db.commit()

	print('CREATE TABLEs rating, user, product')
# create ratings table
	crs.execute('''CREATE TABLE IF NOT EXISTS rating
										(id integer PRIMARY KEY,
										productid text, userid text, score real, text text)''')
	# create users table
	crs.execute('''CREATE TABLE IF NOT EXISTS user
										(id text PRIMARY KEY, num_rating int, av_score real, var_score real)''')
	# create products table
	crs.execute('''CREATE TABLE IF NOT EXISTS product
										(id text PRIMARY KEY, num_rating int, av_score real, var_score real)''')
	db.commit()

	db.close()


def calculate_variance(user_data):
	numerator = 0
	for rate in map(float, user_data[3]):
		numerator += (rate - user_data[1]) * (rate - user_data[1])
	return numerator / float(user_data[2])


def import_dataset(filename):
	# connect to database
	db = sqlite3.connect('dataset/dataset.db')
	crs = db.cursor()


	# RATINGS
	print('INSERT INTO rating')
	# setup progress bar
	len_dataset = sum(1 for row in open(filename, 'r', encoding='utf-8', errors='ignore'))
	prgbar = ProgressBar(40, len_dataset)
	# read dataset
	with open(filename, 'r', encoding='utf-8', errors='ignore') as food:
		dataset = csv.reader(food, delimiter='\n')
		# jump first row
		next(dataset)
		# for each row, insert values in db
		for index, row in enumerate(dataset):
			x = row[0].split('\t')
			crs.execute("INSERT INTO rating VALUES (?,?,?,?,?)", (index, str(x[0]), str(x[1]), x[2], str(x[3])))
			prgbar.step()
	db.commit()
	print()

	# USERS

<<<<<<< HEAD
	crs.execute("SELECT DISTINCT(userid),AVG(score),count(score),GROUP_CONCAT(score) FROM rating GROUP BY userid")
=======
	crs.execute("SELECT DISTINCT(userid),count(score),AVG(score),GROUP_CONCAT(score) FROM ratings GROUP BY userid")
>>>>>>> master
	list_users = crs.fetchall()
	# setup progress bar
	prgbar = ProgressBar(40, len(list_users))
	print('INSERT INTO user')
	parameters = []
	for user in list_users:

		# create object user_data to store [userid, count, avg, rating_list, var]
		user_data = []
		user_data.append(user[0])
		user_data.append(user[1])
		user_data.append(user[2])
		# get all score ratings of user
		user_data.append(user[3].split(','))
		# calculate variance
		user_data.append(calculate_variance(user_data))
		parameters.append((user_data[0], user_data[1], user_data[2], user_data[4]))
		prgbar.step()
	crs.executemany("INSERT INTO user VALUES (?,?,?,?)", parameters)
	db.commit()

	# PRODUCTS
<<<<<<< HEAD
	crs.execute("SELECT DISTINCT(productid),AVG(score),count(score),GROUP_CONCAT(score) FROM rating GROUP BY productid")
=======
	crs.execute("SELECT DISTINCT(productid),count(score),AVG(score),GROUP_CONCAT(score) FROM ratings GROUP BY productid")
>>>>>>> master
	list_products = crs.fetchall()
	# setup progress bar
	prgbar = ProgressBar(40, len(list_products))
	parameters = []
	print('\nINSERT INTO product')
	for product in list_products:
		# create object product_data to store
		product_data = []
		product_data.append(product[0])
		product_data.append(product[1])
		product_data.append(product[2])
		# get all score ratings of user
		product_data.append(product[3].split(','))
		# calculate variance
		product_data.append(calculate_variance(product_data))
		parameters.append((product_data[0], product_data[1], product_data[2], product_data[4]))
		prgbar.step()
	crs.executemany("INSERT INTO product VALUES (?,?,?,?)", parameters)
	db.commit()
	db.close()
