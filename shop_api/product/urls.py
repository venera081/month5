from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list_create_api_view),
    path('categories/<int:id>/', views.category_detail_api_view),
    path('products/', views.products_list_create_api_view),
    path('products/<int:id>/', views.product_detail_api_view),
    path('reviews/', views.reviews_list_create_api_view),
    path('reviews/<int:id>/', views.review_detail_api_view),
    path('products/reviews/', views.products_with_reviews_api_view)

]