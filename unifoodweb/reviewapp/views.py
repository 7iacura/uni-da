from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.template import loader
from django.core.paginator import Paginator
from django.db.models import Count

from db_manager import *
from sentiment import *
from JST import *

from .models import *


set_database_path('reviewapp.db')


def index(request):

	first_run = request.session.get('first_run', True)

	if first_run:
		print('--> first_run <--')

		request.session.flush()
		initialize_util()
		initialize_dataset()

	if Util.objects.filter(type='dataset').exists():
		# get dataset info
		dt = Util.objects.get(type="dataset")
		# get number of users, products, reviews
		n_users = User.objects.count()
		n_products = Product.objects.count()
		n_reviews = Rating.objects.count()

		context = {
			'dataset': dt.name,
			'users': n_users,
			'products': n_products,
			'reviews': n_reviews,
		}

	else:
		context = {}

	return render(request, 'reviewapp/index.html', context)


def dataset(request):

	# import dataset
	if (request.method == 'POST'
			and request.FILES['file']):

		# save file
		file = request.FILES['file']
		fs = FileSystemStorage()
		dataset_name = fs.save(file.name, file)

		# import dataset from file
		ext = dataset_name.split('.')[-1]
		if ext == 'tsv' or ext == 'csv':
			import_dataset(dataset_name)
		elif ext == 'json':
			import_json(dataset_name)
		fs.delete(file.name)

		dt = Util(type='dataset', name=file.name)
		dt.save()

	if Util.objects.filter(type='dataset').exists():
		# get dataset info
		dt = Util.objects.get(type="dataset")
		# get number of users, products, reviews
		n_users = User.objects.count()
		n_products = Product.objects.count()
		n_reviews = Rating.objects.count()

		dist_rating_users_query = execute_select('SELECT COUNT(*) FROM (SELECT score FROM rating GROUP BY userid) rating GROUP BY score ORDER BY score DESC')
		dist_rating_users = ['Users']
		for q in dist_rating_users_query:
			dist_rating_users.append(q[0])

		dist_rating_products_query = execute_select('SELECT COUNT(*) FROM (SELECT score FROM rating GROUP BY productid) rating GROUP BY score ORDER BY score DESC')
		dist_rating_products = ['Products']
		for q in dist_rating_products_query:
			dist_rating_products.append(q[0])

		dist_rating_reviews_query = execute_select('SELECT COUNT(*) FROM rating GROUP BY score ORDER BY score DESC')
		dist_rating_reviews = ['Reviews']
		for q in dist_rating_reviews_query:
			dist_rating_reviews.append(q[0])

		dist_rating = [
			dist_rating_users,
			dist_rating_products,
			dist_rating_reviews
		]

		context = {
			'dataset': dt.name,
			'n_users': n_users,
			'n_products': n_products,
			'n_reviews': n_reviews,
			'dist_rating': dist_rating,
		}

	else:
		context = { }

	return render(request, 'reviewapp/dataset.html', context)


def dataset_remove(request):

		if Util.objects.filter(type='dataset').exists():
			# get dataset info
			dt = Util.objects.get(type="dataset")

		# initialize dataset
			initialize_dataset()
			initialize_util()

		else:
			context = { }

		return redirect('dataset')


def dashboard(request):

	builted_model = request.session.get('builted_model', False)

	if not builted_model:
		checked_users = request.session.get('checked_users', [])

		if len(checked_users) != 0:

			words = request.session.get('words', 10)
			topics = request.session.get('topics', 5)
			iterations = request.session.get('iterations', 20)

			print('\nUsers: ', len(checked_users))
			print('Words: ', words)
			print('Topics: ', topics)
			print('Iterations: ', iterations, '\n')

			# print('\n==========\n== Calculate user experience ==\n==========\n')
			# calculate_users_experience(checked_users)

			print('\n==========\n== Build JST Model ==\n==========\n')
			buildJstModel(checked_users, int(words), int(topics), int(iterations))
			builted_model = True
			request.session['builted_model'] = builted_model

			context = {
				'builted_model': builted_model,
				'checked_users': checked_users,
				'words': words,
				'topics': topics,
				'iterations': iterations,
			}

		else:
			context = { }

	else:

		if request.method == 'POST':
			request.session.flush()
			builted_model = False
			request.session['builted_model'] = builted_model

			execute_statement('DELETE FROM topic')

		checked_users = request.session.get('checked_users', None)
		words = request.session.get('words', None)
		topics = request.session.get('topics', None)
		iterations = request.session.get('iterations', None)

		context = {
			'builted_model': builted_model,
			'checked_users': checked_users,
			'words': words,
			'topics': topics,
			'iterations': iterations,
		}

	return render(request, 'reviewapp/dashboard.html', context)


def getObjectLists(request, object_list, path_page, more_context=[]):
	template = loader.get_template(path_page)
	paginator = Paginator(object_list, 500)
	page = request.GET.get('page')
	object_in_page = paginator.get_page(page)
	context = {
		'objects': object_in_page,
	}
	for c in more_context:
		context[c['key']] = c['value']

	return HttpResponse(template.render(context, request))


def users(request):
	builted_model = request.session.get('builted_model', False)

	ordering = False
	order_by = request.GET.get('order_by')
	direction = request.GET.get('direction')
	if order_by and direction:
		ordering = order_by.lower()
		if direction == 'desc':
			ordering = '-{}'.format(ordering)

	if not builted_model:

		if (request.method == 'POST'
				and request.POST.getlist('checked_users[]')):

			request.session['checked_users'] = request.POST.getlist('checked_users[]')
			request.session['words'] = request.POST.get('words')
			request.session['topics'] = request.POST.get('topics')
			request.session['iterations'] = request.POST.get('iterations')

			return redirect('dashboard')

		else:
			if ordering:
				object_list = User.objects.all().order_by(ordering)
			else:
				object_list = User.objects.all()

			return getObjectLists(request, object_list, 'reviewapp/users.html')

	else:
		checked_users = request.session.get('checked_users', [])

		if ordering:
			object_list = User.objects.all().filter(id__in=checked_users).order_by(ordering)
		else:
			object_list = User.objects.all().filter(id__in=checked_users)

		more_context = [
			{'key': 'builted_model', 'value': True}
		]

		return getObjectLists(request, object_list, 'reviewapp/users.html', more_context)


def user(request, user_id):

	# getUserDistribution
	user_topic_distribution = getUserDistribution(user_id)
	user_topic_distribution_pos = user_topic_distribution[0]
	user_topic_distribution_neg = user_topic_distribution[1]

	topic_pos_chart = []
	for tpc in user_topic_distribution_pos:
		topic_pos_chart.append(tpc[1])

	topic_neg_chart = []
	for tpc in user_topic_distribution_neg:
		topic_neg_chart.append(tpc[1])

	user = get_object_or_404(User, pk=user_id)

	pos_words = user.pos_words
	if pos_words:
		n_pos_words = []
		for word in user.pos_words.split(","):
			n_pos_words.append(word)
		user.pos_words = n_pos_words

	neg_words = user.neg_words
	if neg_words:
		n_neg_words = []
		for word in user.neg_words.split(","):
			n_neg_words.append(word)
		user.neg_words = n_neg_words

	user.products = execute_select('SELECT DISTINCT(productid) FROM rating WHERE userid = "' + user_id + '"')

	review_pie_data = [[5, 0], [4, 0], [3, 0], [2, 0], [1, 0]]
	review_pie_data_raw = execute_select('SELECT score FROM rating WHERE userid = "' + user_id + '"')
	for r in review_pie_data_raw:
		for v in review_pie_data:
			if r[0] == v[0]:
				v[1] += 1

	checked_users = request.session.get('checked_users', [])
	checked_users_query = '"' + '","'.join(str(u) for u in checked_users) + '"'
	if (len(checked_users) > 0):
		max_experience = execute_select('SELECT MAX(experience) FROM user WHERE id IN (' + checked_users_query + ')')[0]

	context = {
		'user': user,
		'topic_pos': user_topic_distribution_pos,
		'topic_pos_chart': topic_pos_chart,
		'topic_neg': user_topic_distribution_neg,
		'topic_neg_chart': topic_neg_chart,
		'review_pie_data': review_pie_data,
		'max_experience': max_experience,
	}
	return render(request, 'reviewapp/user.html', context)


def user_experience(request, user_id):

	print('\n\ncalculate_user_experience', user_id)
	# calculate_user_experience(user_id)
	calculate_users_experience()

	return redirect('/user/'+user_id)


def products(request):

	ordering = False
	order_by = request.GET.get('order_by')
	direction = request.GET.get('direction')
	if order_by and direction:
		ordering = order_by.lower()
		if direction == 'desc':
			ordering = '-{}'.format(ordering)

	if ordering:
		object_list = Product.objects.all().order_by(ordering)
	else:
		object_list = Product.objects.all()

	return getObjectLists(request, object_list, 'reviewapp/products.html')


def product(request, product_id):
	# getProductDistribution
	product_topic_distribution = getProductDistribution(product_id)
	product_topic_distribution_pos = product_topic_distribution[0]
	product_topic_distribution_neg = product_topic_distribution[1]
	product_topic_distribution_chart = product_topic_distribution[2]

	product = get_object_or_404(Product, pk=product_id)

	word_list = []
	for word in product.words.split(","):
		word_list.append(word)

	product.word_list = word_list

	review_pie_data = [[5, 0], [4, 0], [3, 0], [2, 0], [1, 0]]
	review_pie_data_raw = execute_select('SELECT score FROM rating WHERE productid = "' + product_id + '"')
	for r in review_pie_data_raw:
		for v in review_pie_data:
			if r[0] == v[0]:
				v[1] += 1

	context = {
		'product': product,
		'chart_data': product_topic_distribution_chart,
		'topic_pos': product_topic_distribution_pos,
		'topic_neg': product_topic_distribution_neg,
		'review_pie_data': review_pie_data,
	}
	return render(request, 'reviewapp/product.html', context)


def ratings(request):

	ordering = False
	order_by = request.GET.get('order_by')
	direction = request.GET.get('direction')
	if order_by and direction:
		ordering = order_by.lower()
		if direction == 'desc':
			ordering = '-{}'.format(ordering)

	if ordering:
		object_list = Rating.objects.all().order_by(ordering)
	else:
		object_list = Rating.objects.all()

	return getObjectLists(request, object_list, 'reviewapp/ratings.html')


def rating(request, rating_id):
	review = get_object_or_404(Rating, pk=rating_id)
	return render(request, 'reviewapp/rating.html', {'review': review})


def topics(request):

	ordering = False
	order_by = request.GET.get('order_by')
	direction = request.GET.get('direction')
	if order_by and direction:
		ordering = order_by.lower()
		if direction == 'desc':
			ordering = '-{}'.format(ordering)

	if ordering:
		object_list_s = Topic.objects.all().order_by(ordering)
	else:
		object_list_s = Topic.objects.all()

	object_list = []
	for tpc in object_list_s:
		topic_words = []
		for word in tpc.words.split(","):
			topic_words.append(word)
		tpc.word_list = topic_words
		object_list.append(tpc)

	return getObjectLists(request, object_list, 'reviewapp/topics.html')


def topic(request, topic_id):
	tpc = get_object_or_404(Topic, pk=topic_id)
	word_list = []
	for word in tpc.words.split(","):
		word_list.append(word)

	tpc.word_list = word_list

	context = {
		'topic': tpc,
	}
	return render(request, 'reviewapp/topic.html', context)


