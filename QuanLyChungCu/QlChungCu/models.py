# Chuyển đổi cấu 1 trúc dữ liệu hoặc đối tượng thành 1 định dạng có thể lưu trữ được, có thể chuyển đổi lại thành như ban đầu thông qua quá trình deserialization

from django.db import models
# thừa hưởng thuộc tính của nó nhưng muốn dùng của mình để chứng thực
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        # ordering = ['-id']


class User(AbstractUser):
    class EnumRole(models.TextChoices):
        RESIDENT = 'Resident'
        ADMIN = 'Admin'

    user_role = models.CharField(max_length=20, choices=EnumRole.choices, default=EnumRole.RESIDENT)
    avatar_acount = models.ImageField(upload_to='QlChungCu/%Y/%m', null=True)
    change_password_required = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Băm mật khẩu nếu mật khẩu đã được thiết lập
        if self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Box(BaseModel):
    class EnumStatusBox(models.TextChoices):
        WAITING = 'waiting to receive'
        RECEIVED = 'received'

    stand = models.CharField(max_length=255)
    describe = models.CharField(max_length=255)
    box_status = models.CharField(max_length=50, choices=EnumStatusBox.choices,
                                  default=EnumStatusBox.WAITING)  # trạng thái của Box

    user_admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Goods(BaseModel):
    name_goods = models.CharField(max_length=255)
    img_goods = CloudinaryField()
    received_Goods = models.BooleanField(default=False)
    box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True)


class People(BaseModel):
    name_people = models.CharField(max_length=50)
    birthday = models.DateTimeField(null=True, blank=True)
    sex = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=20)
    expiry = models.IntegerField(null=False)  # Hạn sử dụng nhà
    ApartNum = models.CharField(max_length=20)  # Số nhà

    # car_card = models.OneToOneField(CarCard, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name_people


class CarCard(BaseModel):
    class EnumStatusCard(models.TextChoices):
        UN = 'Unconfimred'
        WAIT = 'Wait_for_confirmation'
        CONFIRMER = 'Confirmed'

    area = models.CharField(max_length=255)
    status_card = models.CharField(max_length=50, choices=EnumStatusCard.choices,
                                   default=EnumStatusCard.WAIT)  # Trạng thái thẻ xe
    vehicle_type = models.CharField(max_length=255, default='motorbike')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    people = models.OneToOneField(People, on_delete=models.CASCADE, null=True)


class Letters(BaseModel):
    title_letter = models.TextField(null=True)
    content = RichTextField(null=True)
    img_letter = CloudinaryField()

    people = models.ForeignKey(People, on_delete=models.SET_NULL, null=True)
    user_admin = models.ManyToManyField(User)

class Bill(BaseModel):
    class EnumStatusBill(models.TextChoices):
        UNPAID = 'Unpaid'
        PAID = 'paid '

    class EnumTypeBill(models.TextChoices):
        ELECTRICITY = 'Electricity'
        WATER = 'Water '
        OTHER = 'Other'

    name_bill = models.CharField(max_length=255)
    money = models.FloatField()
    decription = models.CharField(max_length=255) # ghi chu
    type_bill = models.CharField(max_length=50, choices=EnumTypeBill.choices,
                                 default=EnumTypeBill.OTHER)
    status_bill = models.CharField(max_length=50, choices=EnumStatusBill.choices,
                                   default=EnumStatusBill.UNPAID)

    user_resident = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
