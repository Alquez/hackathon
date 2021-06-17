from django.contrib import admin

from movie_api.models import Category, Movie, Like, Favorite, Image, Review, Basket


class ImageInLineAdmin(admin.TabularInline):
    model = Image
    fields = ('image',)
    max_num = 5




admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Review)
admin.site.register(Basket)
