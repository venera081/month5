from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import (
    CategoryListSerializer, ProductsListSerializer, ReviewsListSerializer,
    ProductValidateSerializer, CategoryDelailSerializer,
    ProductDetailSerializer, ReviewDetailSerializer, ProductWithReviewsSerializer
)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView



class CategoryRetrieveUpddateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDelailSerializer
    lookup_field = 'id'


# @api_view(['GET', 'PUT', 'DELETE'])
# def category_detail_api_view(request, id):
#     try:
#         category = Category.objects.get(id=id)
#     except Category.DoesNotExist:
#         return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         data = CategoryDelailSerializer(category).data
#         return Response(data)

#     elif request.method == 'PUT':
#         category.name = request.data.get('name')
#         category.save()
#         return Response(CategoryDelailSerializer(category).data, status=status.HTTP_200_OK)

#     elif request.method == 'DELETE':
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductValidateSerializer
        return CategoryListSerializer
    
    def perform_create(self, serializer):
        validated = serializer.validated_data
        return Category.objects.create(name=validated['name'])
    

# @api_view(['GET', 'POST'])
# def category_list_create_api_view(request):
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         data = CategoryListSerializer(categories, many=True).data
#         return Response(data, status=status.HTTP_200_OK)

#     elif request.method == 'POST':
#         serializer = ProductValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         category = Category.objects.create(
#             name=serializer.validated_data['name']
#         )
#         return Response(CategoryDelailSerializer(category).data, status=status.HTTP_201_CREATED)


class ProductRetrieveUpddateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'


# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail_api_view(request, id):
#     try:
#         product = Product.objects.get(id=id)
#     except Product.DoesNotExist:
#         return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         data = ProductDetailSerializer(product).data
#         return Response(data)

#     elif request.method == 'PUT':
#         product.title = request.data.get('title')
#         product.description = request.data.get('description')
#         product.price = request.data.get('price')
#         product.category_id = request.data.get('category_id')
#         product.save()
#         return Response(ProductDetailSerializer(product).data, status=status.HTTP_200_OK)

#     elif request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductValidateSerializer
        return ProductsListSerializer
    
    def perform_create(self, serializer):
        validated = serializer.validated_data
        return Product.objects.create(title=validated['title'],
                                      description=validated['description'],
                                      price=validated['price'],
                                      category_id=validated['category_id'])


# @api_view(['GET', 'POST'])
# def products_list_create_api_view(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         data = ProductsListSerializer(products, many=True).data
#         return Response(data, status=status.HTTP_200_OK)

#     elif request.method == 'POST':
#         serializer = ProductValidateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         product = Product.objects.create(
#             title=serializer.validated_data['title'],
#             description=serializer.validated_data['description'],
#             price=serializer.validated_data['price'],
#             category_id=serializer.validated_data['category_id']
#         )
#         return Response(ProductDetailSerializer(product).data, status=status.HTTP_201_CREATED)


class ReviewRetrieveUpddateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    lookup_field = 'id'


# @api_view(['GET', 'PUT', 'DELETE'])
# def review_detail_api_view(request, id):
#     try:
#         review = Review.objects.get(id=id)
#     except Review.DoesNotExist:
#         return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         data = ReviewDetailSerializer(review).data
#         return Response(data)

#     elif request.method == 'PUT':
#         review.text = request.data.get('text')
#         review.stars = request.data.get('stars')
#         review.product_id = request.data.get('product_id')
#         review.save()
#         return Response(ReviewDetailSerializer(review).data, status=status.HTTP_200_OK)

#     elif request.method == 'DELETE':
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewsListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewsListSerializer
        return ReviewsListSerializer
    
    def perform_create(self, serializer):
        validated = serializer.validated_data
        return Review.objects.create(text=validated['text'],
                                     stars=validated['stars'],
                                     product_id=validated['product_id'])


# @api_view(['GET', 'POST'])
# def reviews_list_create_api_view(request):
#     if request.method == 'GET':
#         reviews = Review.objects.all()
#         data = ReviewsListSerializer(reviews, many=True).data
#         return Response(data, status=status.HTTP_200_OK)

#     elif request.method == 'POST':
#         serializer = ReviewsListSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         review = Review.objects.create(
#             text=serializer.validated_data['text'],
#             stars=serializer.validated_data['stars'],
#             product_id=serializer.validated_data['product_id']
#         )
#         return Response(ReviewDetailSerializer(review).data, status=status.HTTP_201_CREATED)


class ProductWithReviewsAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer


# @api_view(['GET'])
# def products_with_reviews_api_view(request):
#     products = Product.objects.all()
#     data = ProductWithReviewsSerializer(products, many=True).data
#     return Response(data, status=status.HTTP_200_OK)
