from rest_framework import serializers
# from category.serializers import CategorySerializer
# from comment.serializers import CommentSerializer
from product.models import Product, Basket, Like, Image, Favorites


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Like
        fields = ('product', 'like', 'owner',)


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    # comments = CommentSerializer(many=True, read_only=True)
    # category = CategorySerializer(many=False, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        # fields = ('title', 'body', 'price', 'quantity', 'owner', 'images', 'likes', 'comments', 'category', )

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        product = Product.objects.create(**validated_data)
        print(images_data.getlist('images'))
        for image in images_data.getlist('images'):
            Image.objects.create(product=product, image=image)
        return product

    def validate(self, attrs):
        return super().validate(attrs)


class BasketSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Basket
        fields = ('product', 'basket', 'owner',)


class FavoritesSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Favorites
        fields = ('product', 'favorites', 'owner',)
