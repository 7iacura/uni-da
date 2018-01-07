from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.template import loader
from django.core.paginator import Paginator
from django.db.models import Count

from db_manager import initialize_util, initialize_dataset, import_dataset

from .models import Util, User, Product, Rating

from chartit import DataPool, Chart


RESET_DB_ON_RUNSERVER = False


if RESET_DB_ON_RUNSERVER:
	initialize_util()
	initialize_dataset()


def index(request):

	if request.method == 'POST' and request.FILES['file']:
		# save file
		file = request.FILES['file']
		fs = FileSystemStorage()
		dataset_name = fs.save(file.name, file)

		# import dataset from file
		import_dataset(dataset_name)
		fs.delete(file.name)

		dt = Util(type='dataset', name=file.name)
		dt.save()

		context = {
			'dataset': file.name,
		}
		return render(request, 'reviewapp/index.html', context)

	else:
		if Util.objects.filter(type='dataset').exists():
			# get dataset info
			dt = Util.objects.get(type="dataset")
			# get user list
			user_list = User.objects.all()[:25]
			# get product list
			product_list = Product.objects.all()[:25]

			# get user rating distribution info
			user_rating_distribution = User.objects.values('num_rating').annotate(Count('num_rating'))
			user_rating_data = DataPool(
				series=[{
					'options': {
						'source': user_rating_distribution
					},
					'terms': [
						'num_rating',
						{'nº users': 'num_rating__count'},
					]
				}]
			)
			user_rating_chart = Chart(
				datasource=user_rating_data,
				series_options=[{
					'options': {
						'type': 'line',
						'stacking': False
					},
					'terms': {
						'num_rating': [
							'nº users',
						]
					}
				}],
				chart_options={
					'title': {
						'text': 'Review number per user'
					},
					'xAxis': {
						'title': {
							'text': 'nº reviews'
						}
					},
					'yAxis': {
						'title': {
							'text': 'nº users'
						}
					}
				},
			)

			# get user score distribution info
			user_score_distribution = User.objects.values('av_score').annotate(Count('av_score'))
			user_score_data = DataPool(
				series=[{
					'options': {
						'source': user_score_distribution
					},
					'terms': [
						'av_score',
						{'nº users': 'av_score__count'},
					]
				}]
			)
			user_score_chart = Chart(
				datasource=user_score_data,
				series_options=[{
					'options': {
						'type': 'line',
						'stacking': False
					},
					'terms': {
						'av_score': [
							'nº users',
						]
					}
				}],
				chart_options={
					'title': {
						'text': 'Average score review per user'
					},
					'xAxis': {
						'title': {
							'text': 'score'
						}
					},
					'yAxis': {
						'title': {
							'text': 'nº users'
						}
					}
				},
			)

			# get product rating distribution info
			product_rating_distribution = Product.objects.values('num_rating').annotate(Count('num_rating'))
			product_rating_data = DataPool(
				series=[{
					'options': {
						'source': product_rating_distribution
					},
					'terms': [
						'num_rating',
						{'nº products': 'num_rating__count'},
					]
				}]
			)
			product_rating_chart = Chart(
				datasource=product_rating_data,
				series_options=[{
					'options': {
						'type': 'line',
						'stacking': False
					},
					'terms': {
						'num_rating': [
							'nº products',
						]
					}
				}],
				chart_options={
					'title': {
						'text': 'Review number per product'
					},
					'xAxis': {
						'title': {
							'text': 'nº reviews'
						}
					},
					'yAxis': {
						'title': {
							'text': 'nº products'
						}
					}
				},
			)

			# get product score distribution info
			product_score_distribution = Product.objects.values('av_score').annotate(Count('av_score'))
			product_score_data = DataPool(
				series=[{
					'options': {
						'source': product_score_distribution
					},
					'terms': [
						'av_score',
						{'nº products': 'av_score__count'},
					]
				}]
			)
			product_score_chart = Chart(
				datasource=product_score_data,
				series_options=[{
					'options': {
						'type': 'line',
						'stacking': False
					},
					'terms': {
						'av_score': [
							'nº products',
						]
					}
				}],
				chart_options={
					'title': {
						'text': 'Average score review per product'
					},
					'xAxis': {
						'title': {
							'text': 'score'
						}
					},
					'yAxis': {
						'title': {
							'text': 'nº products'
						}
					}
				},
			)

			context = {
				'dataset': dt.name,
				'user_list': user_list,
				'product_list': product_list,
				'chart_list': [user_rating_chart, user_score_chart, product_rating_chart, product_score_chart],
			}

		else:
			context = {}

		return render(request, 'reviewapp/index.html', context)


def getObjectLists(request, object_list, path_page):
	template = loader.get_template(path_page)
	paginator = Paginator(object_list, 25)
	page = request.GET.get('page')
	object_in_page = paginator.get_page(page)
	context = {
		'objects': object_in_page,
	}
	return HttpResponse(template.render(context, request))


def users(request):
	object_list = User.objects.all()
	return getObjectLists(request, object_list, 'reviewapp/users.html')


def products(request):
	object_list = Product.objects.all()
	return getObjectLists(request, object_list, 'reviewapp/products.html')


def ratings(request):
	object_list = Rating.objects.all()
	return getObjectLists(request, object_list, 'reviewapp/ratings.html')


def user(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	return render(request, 'reviewapp/user.html', {'user': user})


def product(request, product_id):
	product = get_object_or_404(Product, pk=product_id)
	return render(request, 'reviewapp/product.html', {'product': product})


def rating(request, rating_id):
	review = get_object_or_404(Rating, pk=rating_id)
	return render(request, 'reviewapp/rating.html', {'review': review})


