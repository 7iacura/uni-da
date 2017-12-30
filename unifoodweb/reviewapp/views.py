from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator

# from django.shortcuts import get_list_or_404, get_object_or_404

from .models import User, Product, Rating


def index(request):
	template = loader.get_template('reviewapp/index.html')
	context = { }
	return HttpResponse(template.render(context, request))


def users(request):
	object_list = User.objects.all()
	template = loader.get_template('reviewapp/users.html')
	paginator = Paginator(object_list, 25)
	page = request.GET.get('page')
	object_in_page = paginator.get_page(page)
	context = {
		'objects': object_in_page,
	}
	return HttpResponse(template.render(context, request))


def user(request, user_id):
	return HttpResponse("Detail of user %s here" % user_id)


def products(request):
	product_list = Product.objects.all()
	template = loader.get_template('reviewapp/products.html')
	paginator = Paginator(product_list, 25)
	page = request.GET.get('page')
	product_page = paginator.get_page(page)
	context = {
		'objects': product_page,
	}
	return HttpResponse(template.render(context, request))


def product(request, product_id):
	return HttpResponse("Detail of product %s here" % product_id)


def ratings(request):
	review_list = Rating.objects.all()
	template = loader.get_template('reviewapp/ratings.html')
	paginator = Paginator(review_list, 25)
	page = request.GET.get('page')
	review_page = paginator.get_page(page)
	context = {
		'objects': review_page,
	}
	return HttpResponse(template.render(context, request))


def rating(request, rating_id):
	return HttpResponse("Detail of rating %s here" % rating_id)


# def index(request):
# 	template = loader.get_template('reviewapp/templates/index.html')
# 	return HttpResponse(template.render(request))