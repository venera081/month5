from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreateAPIView.as_view()),
    path('categories/<int:id>/', views.CategoryRetrieveUpddateDestroyAPIView.as_view()),
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/<int:id>/', views.ProductRetrieveUpddateDestroyAPIView.as_view()),
    path('reviews/', views.ReviewListCreateAPIView.as_view()),
    path('reviews/<int:id>/', views.ReviewRetrieveUpddateDestroyAPIView.as_view()),
    path('products/reviews/', views.ProductWithReviewsAPIView.as_view())
]