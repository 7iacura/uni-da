from django.urls import path
from . import views


urlpatterns = [

    # /reviewapp/
    path('', views.index, name='index'),

    # /import-dataset/
    path('import-dataset', views.importdataset, name='importdataset'),

    # /users/
    path('users/', views.users, name='users'),
    # /user/0/
    path('user/<str:user_id>', views.user, name='user'),

    # /products/
    path('products/', views.products, name='products'),
    # /product/0/
    path('product/<str:product_id>', views.product, name='product'),

    # /ratings/
    path('ratings/', views.ratings, name='ratings'),
    # /rating/0/
    path('rating/<int:rating_id>', views.rating, name='rating'),
]

