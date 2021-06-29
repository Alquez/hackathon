from django.db import models
from account.serializers import User


class Product(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField(blank=True)
    image = models.ImageField()
    price = models.PositiveIntegerField()
    owner = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE, default=True)

    def __str__(self):
        return f'{self.title}'


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField()

    class Meta:
        unique_together = ['owner', 'product']


class Basket(models.Model):
    owner = models.ForeignKey(User, related_name='basket', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='basket')
    basket = models.BooleanField()

    class Meta:
        unique_together = ['owner', 'product']


class Favorites(models.Model):
    owner = models.ForeignKey(User, related_name='favorites', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorites = models.BooleanField()

    class Meta:
        unique_together = ['owner', 'product']