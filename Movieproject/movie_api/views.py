from django.contrib.auth.decorators import login_required
from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
# from rest_framework.views import APIView
from .models import Category, Movie, Review, Like, Favorite, Basket
from .serializers import CategoryListSerializer, MovieSerializer, ReviewSerializer, \
    CategoryDetailSerializer, FavoriteSerializer, BasketSerializer, LikeSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .permissions import IsAuthorMoviePermission, IsProducerPermission, IsCustomerPermission, IsAuthorReviewPermission
from django_filters.rest_framework import DjangoFilterBackend


class PaginationMovie(PageNumberPagination):
    page_size = 2

class PaginationReview(PageNumberPagination):
    page_size = 2



class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [AllowAny, ]

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer




class PermissionMixinMovie:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsProducerPermission, ]
        elif self.action in ['update', 'partial_update', 'delete']:
            permissions = [IsAuthorMoviePermission, ]
        else:
            permissions = [AllowAny, ]
        return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}

class PermissionMixinReview:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsCustomerPermission, ]
        elif self.action in ['update', 'partial_update', 'delete']:
            permissions = [IsAuthorReviewPermission, ]
        else:
            permissions = [AllowAny, ]
        return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}



class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = PaginationMovie
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', ]

    # @login_required
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        movie = self.get_object()
        obj, created = Like.objects.get_or_create(user=request.user.profile_customer, movie=movie)
        if not created:
            obj.like = not obj.like
            obj.save()
        liked_or_disliked = 'liked' if obj.like else 'disliked'
        return Response('Successfully {} product'.format(liked_or_disliked), status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        movie = self.get_object()
        obj, created = Favorite.objects.get_or_create(user=request.user.profile_customer, movie=movie)
        if not created:
            obj.favorite = not obj.favorite
            obj.save()
        added_removed = 'added' if obj.favorite else 'removed'
        return Response('Successfully {} favorite'.format(added_removed), status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'])
    def basket(self, request, pk=None):
        movie = self.get_object()
        obj, created = Basket.objects.get_or_create(user=request.user.profile_customer, movie=movie)
        if not created:
            obj.favorite = not obj.favorite
            obj.save()
        added_removed = 'added' if obj.favorite else 'removed'
        return Response('Successfully {} basket'.format(added_removed), status=status.HTTP_200_OK)




    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q', '')
        # q = request.GET.get('q', None)
        print('hello')
        queryset = self.get_queryset()
        print(queryset)
        queryset = queryset.filter(Q(title__icontains=q) | Q(id__icontains=q))
        # print(queryset)
        # queryset = queryset.filter(Q(description__icontains=q))
        serializer = MovieSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # @action(detail=True, methods=['get'])
    # def search_product(request, pk=None):
    #     """ search function  """
    #     if request.method == "POST":
    #         query_name = request.POST.get('title', None)
    #         if query_name:
    #             results = Movie.objects.filter(title__contains=query_name)
    #             return render(request, results, {"results": results})
    #
    #     return Response(serializer.data, status=status.HTTP_200_OK)




class ReviewViewSet(PermissionMixinReview, viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PaginationReview


class LikeCreateListView(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_queryset(self):
        qs = self.request.user.profile_customer
        queryset = Favorite.objects.filter(user=qs, like=True)
        return queryset

class FavoriteListView(generics.ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        qs = self.request.user.profile_customer
        queryset = Favorite.objects.filter(user=qs, favorite=True)
        return queryset

class BasketListView(generics.ListAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer

    def get_queryset(self):
        qs = self.request.user.profile_customer
        queryset = Basket.objects.filter(user=qs, basket=True)
        return queryset
















