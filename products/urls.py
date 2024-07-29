from django.urls import path
from .views import (
    CategoryProductsListView,
    ShoesListView,
    ShoesListView1,
    ShoesDetailView,
    ShoesUpdateView,
    ShoesDeleteView,
    AddReviewView,
    ReviewDeleteView,
    ReviewUpdateView,
    CreateShoeView,
    SearchView,
    FilterView,
)

app_name = 'products'

urlpatterns = [
    path('category_products/', CategoryProductsListView.as_view(), name='category_products'),
    path('categories/<int:category_id>/', ShoesListView.as_view(), name='shoes_by_category'),
    path('shoes/', ShoesListView1.as_view(), name='shoes_list'),
    path('shoes/<int:pk>/', ShoesDetailView.as_view(), name='shoe_detail'),
    path('shoes/<int:pk>/edit/', ShoesUpdateView.as_view(), name='shoes_update'),
    path('shoes/<int:pk>/delete/', ShoesDeleteView.as_view(), name='shoes_delete'),
    path('shoes/<int:pk>/add_review/', AddReviewView.as_view(), name='add_review'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='delete_review'),
    path('review/<int:pk>/update/', ReviewUpdateView.as_view(), name='update_review'),
    path('products/create/', CreateShoeView.as_view(), name='createshoe'),
    path('search/', SearchView.as_view(), name='search'),
    path('filter/', FilterView.as_view(), name='filter'),
]
