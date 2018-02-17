from django.db import models


class Util(models.Model):
	id = models.IntegerField(primary_key=True)
	type = models.TextField(blank=True, null=True)
	name = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.id

	class Meta:
		managed = False
		db_table = 'utils'


class Product(models.Model):
	id = models.TextField(primary_key=True)
	num_rating = models.IntegerField(blank=True, null=True)
	av_score = models.FloatField(blank=True, null=True)
	var_score = models.FloatField(blank=True, null=True)
	words = models.FloatField(blank=True, null=True)

	def __str__(self):
		return self.id

	class Meta:
		managed = False
		db_table = 'product'


class Rating(models.Model):
	id = models.IntegerField(primary_key=True)
	productid = models.TextField(blank=True, null=True)
	userid = models.TextField(blank=True, null=True)
	score = models.FloatField(blank=True, null=True)
	text = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.id

	class Meta:
		managed = False
		db_table = 'rating'


class User(models.Model):
	id = models.TextField(primary_key=True)
	num_rating = models.IntegerField(blank=True, null=True)
	av_score = models.FloatField(blank=True, null=True)
	var_score = models.FloatField(blank=True, null=True)
	experience = models.FloatField(blank=True, null=True)
	experience_level = models.FloatField(blank=True, null=True)
	pos_words = models.FloatField(blank=True, null=True)
	neg_words = models.FloatField(blank=True, null=True)

	def __str__(self):
		return self.id

	class Meta:
		managed = False
		db_table = 'user'


class Topic(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.TextField(blank=True, null=True)
	sentiment = models.TextField(blank=True, null=True)
	words = models.FloatField(blank=True, null=True)

	def __str__(self):
		return self.id

	class Meta:
		managed = False
		db_table = 'topic'
