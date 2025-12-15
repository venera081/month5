from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination
from common.permissions import IsModerator
from common.validators import validate_age
from .models import Category, Product, Review
from .serializers import (
    CategoryListSerializer, ProductsListSerializer, ReviewsListSerializer,
    ProductValidateSerializer, CategoryDelailSerializer,
    ProductDetailSerializer, ReviewDetailSerializer, ProductWithReviewsSerializer,
    CategoryValidateSerializer
)
from .tasks import generate_product_code, notify_new_category

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
        category = Category.objects.create(name=validated['name'])

        notify_new_category.delay(category.id)

        return category
    
    def get(self, request, *args, **kwargs):
        cached_data = cache.get("category_list")
        if cached_data:
            return Response(data=cached_data, status=status.HTTP_200_OK)
        response = super().get(self, request, *args, **kwargs)
        if response.data.get("count", 0) > 0:
            cache.set("category_list", response.data, timeout=300)
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
        product = Product.objects.create(
            title=validated['title'],
            description=validated['description'],
            price=validated['price'],
            category_id=validated['category_id']
        )

        generate_product_code.delay(product.id)

        return product

class ReviewRetrieveUpddateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    lookup_field = 'id'


class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewsListSerializer
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        return ReviewsListSerializer
    
    def perform_create(self, serializer):
        validated = serializer.validated_data
        return Review.objects.create(
            text=validated['text'],
            stars=validated['stars'],
            product_id=validated['product_id']
        )


class ProductWithReviewsAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer
