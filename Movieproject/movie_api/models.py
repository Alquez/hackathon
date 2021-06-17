from django.contrib.auth import get_user_model
from django.db import models
from movieprofile.models import ProfileProducer, ProfileCustomer

CustomUser = get_user_model()

class Category(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50)
    name = models.CharField(max_length=250)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.parent:
            return f'{self.parent} ... {self.name}'
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    @property
    def get_children(self):
        if self.children:
            return self.children.all()
        return False


class Movie(models.Model):
    author = models.ForeignKey(ProfileProducer, on_delete=models.CASCADE, related_name='movies')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='movies')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return f'{self.title}--{self.created}'

    class Meta:
        ordering = ('created',)

class Image(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='movie/')


class Review(models.Model):
    user = models.ForeignKey(ProfileCustomer, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}--{self.movie}--{self.created}--{self.body[0:10]}'

    class Meta:
        ordering = ('created', )

class Like(models.Model):
    user = models.ForeignKey(ProfileCustomer, on_delete=models.CASCADE, related_name='likes')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes')
    likes_number = models.AutoField(primary_key=True)
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} liked this movie--> {self.movie}'


class Favorite(models.Model):
    user = models.ForeignKey(ProfileCustomer, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} added to favorite'


class Basket(models.Model):
    user = models.ForeignKey(ProfileCustomer, on_delete=models.CASCADE, related_name='baskets')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='baskets')
    basket = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} added to basket'