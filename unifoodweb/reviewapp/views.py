# from django.shortcuts import render
from django.http import HttpResponse
# from django.template import loader

def index(request):
	return HttpResponse("Hello, world. Here we put a graphic fiqua.")


def users(request):
	return HttpResponse("List of users here")


def user(request, user_id):
	return HttpResponse("Detail of user %s here" % user_id)


def products(request):
	return HttpResponse("List of products here")


def product(request, product_id):
	return HttpResponse("Detail of product %s here" % product_id)


def ratings(request):
	return HttpResponse("List of ratings here")


def rating(request, rating_id):
	return HttpResponse("Detail of rating %s here" % rating_id)


# def index(request):
# 	template = loader.get_template('reviewapp/templates/index.html')
# 	return HttpResponse(template.render(request))