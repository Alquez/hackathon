from rest_framework import serializers
from .models import *

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('slug', 'name', )

    def to_representation(self, instance):
        representation = super(CategoryDetailSerializer, self).to_representation(instance)
        return representation

class MovieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', )

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class MovieSerializer(serializers.ModelSerializer):
    images = MovieImageSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'description', 'price', 'category', 'images')

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        user = request.user.profile_producer
        product = Movie.objects.create(author=user, **validated_data)
        for image in images_data.getlist('images'):
            Image.objects.create(product=product, image=image)
        return product

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.images.all().delete()
        images_data = request.FILES
        for image in images_data.getlist('images'):
            Image.objects.create(product=instance, image=image)
        return instance

    def to_representation(self, instance):
        representation = super(MovieSerializer, self).to_representation(instance)
        action = self.context.get('action')
        reviews = ReviewSerializer(instance.reviews.all(), many=True).data
        likes = LikeSerializer(instance.likes.filter(like=True), many=True).data
        representation['author'] = instance.author.email
        representation['images'] = MovieImageSerializer(instance.images.all(), many=True, context=self.context).data
        if action == 'list':
            representation['reviews'] = len(reviews)
            representation['likes'] = len(likes)
        if action == 'retrieve':
            representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
            representation['likes'] = LikeSerializer(instance.likes.filter(like=True), many=True).data
        return representation



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'movie', 'body', )

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user.profile_customer
        review = Review.objects.create(user=user, **validated_data)
        return review

    def to_representation(self, instance):
        representation = super(ReviewSerializer, self).to_representation(instance)
        representation['user'] = instance.user.email
        return representation


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        return representation


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = '__all__'
