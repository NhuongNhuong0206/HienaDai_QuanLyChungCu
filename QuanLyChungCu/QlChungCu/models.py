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


class AcountAdmin(BaseModel):
    nameacount_admin = models.CharField(max_length=25, null=True)
    passacount_admin = models.CharField(max_length=25,null=True)
    area_admin = models.CharField(max_length=255, null=True)


class Car_card(BaseModel):
    area = models.CharField(max_length=255)

    admin = models.ForeignKey(AcountAdmin, on_delete=models.SET_NULL, null=True)


class Acount(BaseModel):
    name_acount = models.CharField(max_length=25)
    pass_acount = models.CharField(max_length=25)
    avatar_acount = models.ImageField(upload_to='QlChungCu/%Y/%m')

    admin = models.ForeignKey(AcountAdmin, on_delete=models.SET_NULL, null=True)


class Box(BaseModel):
    stand = models.CharField(max_length=255)
    describe = models.CharField(max_length=255)

    admin = models.ForeignKey(AcountAdmin, on_delete=models.SET_NULL, null=True)


class Goods(BaseModel):
    name_goods = models.CharField(max_length=255)
    img_goods = CloudinaryField()

    box = models.ForeignKey(Box,on_delete=models.SET_NULL, null=True)


class People(BaseModel):
    name_people = models.CharField(max_length=50)
    birthday = models.DateTimeField(null=True, blank=True)
    sex = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=20)
    expiry = models.IntegerField(null=False)#Hạn sử dụng nhà
    ApartNum = models.CharField(max_length=20)#Số nhà

    car_card = models.OneToOneField(Car_card, on_delete=models.CASCADE)
    acount = models.OneToOneField(Acount, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name_people


class Letters(BaseModel):
    title_letter = models.TextField()
    content = models.TextField()
    img_letter = CloudinaryField()

    people = models.ForeignKey(People, on_delete=models.SET_NULL, null=True)
    admin = models.ManyToManyField(AcountAdmin)


class Bill(BaseModel):
    name_bill = models.CharField(max_length=255)
    money = models.FloatField()
    decription = models.CharField(max_length=255)
    type_bill = models.FloatField(default=3)# 1: Phí tiền điện, 2: Phí tiền nước, 3: Phí khác

    Acount_id = models.ForeignKey(Acount, on_delete=models.SET_NULL, null=True)

    


