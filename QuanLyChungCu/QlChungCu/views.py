from django.shortcuts import render
from rest_framework import viewsets
from .models import AcountAdmin, People, Car_card, Acount, Box, Goods, Letters, Bill
from .serializers import PeopleSerializers, AcountAdminSerializers, Car_cardSerializers, AcountSerializers, \
    BoxSerializers, GoodsSerializers, LettersSerializers, BillSerializers


# ModelViewSet Kế thừa APIview, APIview kế thừa tiêu chuẩn của django
# ModelViewSet implament 1 số thứ sẵn từ model
# ModelViewSet chỉ cần chỉ định 2 th:  + Queryset: Câu truy vấn dựa vào đổ lên model cho mình
#                                      + serializer: pare danh sách lấy được ở queryset ra bên ngoài, và create update, retrofit


class AcountAdminViewset(viewsets.ModelViewSet):
    queryset = AcountAdmin.objects.filter(active=True)  # Lấy các tài khoản cư dân đang active
    serializer_class = AcountAdminSerializers
    # Tạo 5 API:
    # List (GET) --> Xem danh sách Tài khoản cư dan
    # ... (POST) --> Thêm cư dân
    # detail --> Xem chi tiết thông tin Tài khoản cư dân
    # ... --> Cập nhập
    # ... (DELETE) --> Xoá Tài khoản cư dân


class PeopleViewset(viewsets.ModelViewSet):
    queryset = People.objects.filter(active=True)
    serializer_class = PeopleSerializers


class Car_cardViewset(viewsets.ModelViewSet):
    queryset = Car_card.objects.filter(active=True)
    serializer_class = Car_cardSerializers

class AcountViewset(viewsets.ModelViewSet):
        queryset = Acount.objects.filter(active=True)
        serializer_class = AcountSerializers


class BoxViewset(viewsets.ModelViewSet):
    queryset = Box.objects.filter(active=True)
    serializer_class = BoxSerializers


class GoodsViewset(viewsets.ModelViewSet):
    queryset = Goods.objects.filter(active=True)
    serializer_class = GoodsSerializers


class LettersViewset(viewsets.ModelViewSet):
    queryset = Letters.objects.filter(active=True)
    serializer_class = LettersSerializers


class BillViewset(viewsets.ModelViewSet):
    queryset = Bill.objects.filter(active=True)
    serializer_class = BillSerializers