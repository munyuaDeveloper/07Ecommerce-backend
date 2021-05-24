from rest_framework import generics

from property.models import Property
from property.serializers import PropertySerializer


class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
