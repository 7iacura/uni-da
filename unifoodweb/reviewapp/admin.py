from django.contrib import admin

from .models import User
from .models import Product
from .models import Rating


class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'num_rating', 'av_score', 'var_score')


class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', 'num_rating', 'av_score', 'var_score')


class RatingAdmin(admin.ModelAdmin):
	list_display = ('id', 'productid', 'userid', 'score', 'text')


admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Rating, RatingAdmin)
