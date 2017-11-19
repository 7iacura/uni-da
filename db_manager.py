import sqlite3
import csv


def initialize_dataset():
	# connect to (or create) database
	db = sqlite3.connect('dataset/dataset.db')
	# create cursor
	cursor = db.cursor()

	# clean db of dataset
	cursor.execute('DROP TABLE IF EXISTS products')
	db.commit()
	print('DROP TABLE products')

	cursor.execute('DROP TABLE IF EXISTS users')
	db.commit()
	print('DROP TABLE users')

	cursor.execute('DROP TABLE IF EXISTS ratings')
	db.commit()
	print('DROP TABLE ratings')

	# create ratings table
	cursor.execute('''CREATE TABLE IF NOT EXISTS ratings
										(id integer PRIMARY KEY,
										productid text, userid text, score real, text text)''')
	db.commit()
	print('CREATE TABLE ratings')

# create users table
	cursor.execute('''CREATE TABLE IF NOT EXISTS users
										(userid text PRIMARY KEY, num_rating int, av_score real, var_score real)''')
	db.commit()
	print('CREATE TABLE users')

	# create products table
	cursor.execute('''CREATE TABLE IF NOT EXISTS products
										(productid text PRIMARY KEY, num_rating int, av_score real, var_score real)''')
	db.commit()
	print('CREATE TABLE users')

	db.close()


def import_dataset():
	# connect to database
	db = sqlite3.connect('dataset/dataset.db')
	# create cursor
	cursor = db.cursor()

	# read dataset
	with open('dataset/food.tsv', 'r', encoding='utf-8', errors='ignore') as food:
		dataset = csv.reader(food, delimiter='\n')
		print('Read tsv dataset')
		# jump first row
		next(dataset)
	# for each row, insert values in db
		for index, row in enumerate(dataset):
			data = row[0].split('\t')
			cursor.execute("INSERT INTO ratings VALUES (?,?,?,?,?)", (index, str(data[0]), str(data[1]), data[2], str(data[3])))
	db.commit()
	print('INSERT INTO ratings')

	# for user in cursor.execute("SELECT DISTINCT(userid) FROM ratings"):
	# 	cursor.execute("SELECT COUNT(score), AVG(score) FROM ratings WHERE userid = ?", (user))
	#
	#
	# for product in cursor.execute("SELECT DISTINCT(productid) FROM ratings"):
	# 	cursor.execute("SELECT COUNT(score), AVG(score) FROM ratings WHERE productid = ?", (product))

	db.close()
