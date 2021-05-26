from category.views import (
    CategoryListView, CategoryCreateView, ListCategoryItemView)
from django.conf.urls import url


urlpatterns = [
    url('category-list', CategoryListView.as_view(), name='category-list'),
    url('category-products', ListCategoryItemView.as_view(),
        name='category-products'),
    url('create-category', CategoryCreateView.as_view(), name='create-category'),
]
