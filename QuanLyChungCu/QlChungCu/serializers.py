from QlChungCu.models import People
from rest_framework import serializers


class PeopleSerializers(serializers.ModelSerializer):
    class Meta:

        model = People
        fields = '__all__'
