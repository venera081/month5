from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import (
    CategoryListSerializer, ProductsListSerializer, ReviewsListSerializer,
    ProductValidateSerializer, CategoryDelailSerializer,
    ProductDetailSerializer, ReviewDetailSerializer, ProductWithReviewsSerializer,
    CategoryValidateSerializer
)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from common.permissions import IsModerator
from common.validators import validate_age
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination

PAGE_SIZE = 5

class CategoryRetrieveUpddateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDelailSerializer
    lookup_field = 'id'
    


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    permission_classes = [IsModerator]
    pagination_class = PageNumberPagination


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryValidateSerializer
        return CategoryListSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        validate_age(user)
        validated = serializer.validated_data
        return Category.objects.create(name=validated['name'])
    
    def get(self, request, *args, **kwargs):
        cached_data = cache.get("product_list")
        if cached_data:
            print("Redis")
            return Response(data=cached_data, status=status.HTTP_200_OK)
        response = super().get(self, request, *args, **kwargs)
        print("Postgres")
        if response.data.get("count", 0) > 0:
            cache.set("product_list", response.data, timeout=300)
        return response

class ProductRetrieveUpddateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'
    
    
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsListSerializer
    permission_classes = [IsModerator]
    pagination_class = PageNumberPagination


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductValidateSerializer
        return ProductsListSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        validate_age(user)
        validated = serializer.validated_data
        return Product.objects.create(title=validated['title'],
                                      description=validated['description'],
                                      price=validated['price'],
                                      category_id=validated['category_id'])

    

class ReviewRetrieveUpddateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    lookup_field = 'id'



class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewsListSerializer
    pagination_class = PageNumberPagination

    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewsListSerializer
        return ReviewsListSerializer
    
    def perform_create(self, serializer):
        validated = serializer.validated_data
        return Review.objects.create(text=validated['text'],
                                     stars=validated['stars'],
                                     product_id=validated['product_id'])


class ProductWithReviewsAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer


