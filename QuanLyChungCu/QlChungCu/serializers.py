from QlChungCu.models import People
from rest_framework import serializers


class PeopleSerializers(serializers.ModelSerializer):
    class Meta:

        moder = People
        filter = '__all__'
