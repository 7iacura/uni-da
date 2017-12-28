from django.urls import path

from . import views

# urlpatterns = [
#     # ex: /polls/
#     path('', views.index, name='index'),
#     # ex: /polls/5/
#     path('<int:question_id>/', views.detail, name='detail'),
#     # ex: /polls/5/results/
#     path('<int:question_id>/results/', views.results, name='results'),
#     # ex: /polls/5/vote/
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]

urlpatterns = [

    # /reviewapp/
    path('', views.index, name='index'),

    # /users/
    path('users/', views.users, name='users'),
    # /user/0/
    path('user/<int:user_id>', views.user, name='user'),

    # /products/
    path('products/', views.products, name='products'),
    # /product/0/
    path('product/<int:product_id>', views.product, name='product'),

    # /ratings/
    path('ratings/', views.ratings, name='ratings'),
    # /rating/0/
    path('rating/<int:rating_id>', views.rating, name='rating'),
]

