from django.conf.urls import url

from property.views import PropertyListView

urlpatterns = [
    url('properties/', PropertyListView.as_view(), name='property-list'),
]
