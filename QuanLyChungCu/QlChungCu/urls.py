from rest_framework import viewsets, generics
from QlChungCu.models import People
from QlChungCu import serializers


class PeopleViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = People.object.filter