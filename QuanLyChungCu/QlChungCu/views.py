from rest_framework import viewsets, generics
from QlChungCu.models import People
from QlChungCu import serializers, paginators


class PeopleViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = People.objects.filter(active = True)
    serializer_class = serializers.PeopleSerializers
    pagination_class = paginators.PeoplePaginator