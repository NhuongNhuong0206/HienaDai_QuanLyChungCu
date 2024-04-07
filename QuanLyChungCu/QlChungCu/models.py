# Chuyển đổi cấu 1 trúc dữ liệu hoặc đối tượng thành 1 định dạng có thể lưu trữ được, có thể chuyển đổi lại thành như ban đầu thông qua quá trình deserialization

from django.db import models
# thừa hưởng thuộc tính của nó nhưng muốn dùng của mình để chứng thực
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    pass


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        # ordering = ['-id']


class Admin(BaseModel):
    area_admin = models.CharField(max_length=255)


class Car_card(BaseModel):
    area = models.CharField(max_length=255)

    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)


class Acount(BaseModel):
    name_acount = models.CharField(max_length=25)
    pass_acount = models.CharField(max_length=25)
    avatar_acount = models.CharField(max_length=255)

    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)


class Box(BaseModel):
    stand = models.CharField(max_length=255)
    describe = models.CharField(max_length=255)

    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)


class Goods(BaseModel):
    name_goods = models.CharField(max_length=255)
    img_goods = CloudinaryField()

    box = models.ForeignKey(Box,on_delete=models.SET_NULL, null=True)


class People(BaseModel):
    name_people = models.CharField(max_length=50, default=None)
    birthday = models.DateTimeField(null=True, blank=True, default=None)
    sex = models.CharField(max_length=20, default=None)
    phone = models.CharField(max_length=20, null=False, default=None)
    email = models.CharField(max_length=20, default=None)
    expiry = models.IntegerField(null=False, default=None)#Hạn sử dụng nhà
    ApartNum = models.CharField(max_length=20, default=None)#Số nhà

    car_card = models.OneToOneField(Car_card, on_delete=models.CASCADE, default=None)
    acount = models.OneToOneField(Acount, on_delete=models.CASCADE, default=None)
    box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name_user


class Letters(BaseModel):
    title_letter = models.TextField()
    content = models.TextField()
    img_letter = CloudinaryField()

    people = models.ForeignKey(People, on_delete=models.SET_NULL, null=True)
    admin = models.ManyToManyField(Admin)


class Bill(BaseModel):
    name_bill = models.CharField(max_length=255)
    money = models.FloatField()
    decription = models.CharField(max_length=255)

    people = models.ForeignKey(People, on_delete=models.SET_NULL, null=True)

    


