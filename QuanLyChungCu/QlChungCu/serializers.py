#serializers chuyển dữ liệu phức tạp từ Queryset thành kiểu dữ liệu đơn gian như Json để chuyển ra bên ngoài
#Có nhiều cách khai báo serializer: + Không cần model
#                                   + liên kết với model: ở đây sử dụng cách này

from QlChungCu.models import People, AcountAdmin, Car_card, Acount, Box, Goods, Letters, Bill
from rest_framework import serializers


class PeopleSerializers(serializers.ModelSerializer):
    class Meta:
        model = People
        # filter chỉ định các trường serialize ra pare thành json để gửi ra bên ngoài để client gọi API
        fields = '__all__'


class AcountAdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = AcountAdmin
        # filter chỉ định các trường serialize ra pare thành json để gửi ra bên ngoài để client gọi API
        fields = '__all__'


class Car_cardSerializers(serializers.ModelSerializer):
    class Meta:
        model = Car_card
        # filter chỉ định các trường serialize ra pare thành json để gửi ra bên ngoài để client gọi API
        fields = '__all__'


class AcountSerializers(serializers.ModelSerializer):
    class Meta:
        model = Acount
        # filter chỉ định các trường serialize ra pare thành json để gửi ra bên ngoài để client gọi API
        fields = '__all__'


class BoxSerializers(serializers.ModelSerializer):
    class Meta:
        model = Box
        # filter chỉ định các trường serialize ra pare thành json để gửi ra bên ngoài để client gọi API
        fields = '__all__'


class GoodsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Goods
        # filter chỉ định các trường serialize ra pare thành json để gửi ra bên ngoài để client gọi API
        fields = '__all__'


class LettersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Letters
        # filter chỉ định các trường serialize ra pare thành json để gửi ra bên ngoài để client gọi API
        fields = '__all__'


class BillSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bill
        # filter chỉ định các trường serialize ra pare thành json để gửi ra bên ngoài để client gọi API
        fields = '__all__'