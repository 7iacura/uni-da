from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
	return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, user_id):
	return HttpResponse("You're looking at user %s." % user_id)

# def index(request):
# 	template = loader.get_template('reviewapp/templates/index.html')
# 	return HttpResponse(template.render(request))