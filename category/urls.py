from category.views import CategoryListView, CategoryCreateView
from django.conf.urls import url


urlpatterns = [
    url('category-list', CategoryListView.as_view(), name='category-list'),
    url('create-category', CategoryCreateView.as_view(), name='create-category'),
]
