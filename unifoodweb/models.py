from django.db import models


class Products(models.Model):
    productid = models.TextField(unique=True, blank=True, null=True)
    num_rating = models.IntegerField(blank=True, null=True)
    av_score = models.FloatField(blank=True, null=True)
    var_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class Ratings(models.Model):
    id = models.IntegerField(blank=True, null=True)
    productid = models.TextField(blank=True, null=True)
    userid = models.TextField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ratings'


class Users(models.Model):
    userid = models.TextField(unique=True, blank=True, null=True)
    num_rating = models.IntegerField(blank=True, null=True)
    av_score = models.FloatField(blank=True, null=True)
    var_score = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
