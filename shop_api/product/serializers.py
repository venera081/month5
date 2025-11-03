from rest_framework import serializers
from .models import Category, Product, Review



class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source='product_set.count', read_only=True)
    class Meta:
        model = Category
        fields = 'id name products_count'.split()

class ProductsListSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id reviews title description'.split()

    def get_reviews(self, product):
        l = []
        for i in product.reviews.all():
            l.append(i.text)
        return l

class ReviewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars'.split()

class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewsListSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id title description reviews rating'.split()

    def get_rating(self, obj):
        return obj.average_rating()



class CategoryDelailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'