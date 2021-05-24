from category.views import CategoryListView
from django.conf.urls import url


urlpatterns = [
    url('category-list', CategoryListView.as_view(), name='category-list'),
]
