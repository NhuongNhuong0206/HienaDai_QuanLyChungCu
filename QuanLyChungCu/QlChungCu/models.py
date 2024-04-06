# Chuyển đổi cấu 1 trúc dữ liệu hoặc đối tượng thành 1 định dạng có thể lưu trữ được, có thể chuyển đổi lại thành như ban đầu thông qua quá trình deserialization

from django.db import models
# thừa hưởng thuộc tính của nó nhưng muốn dùng của mình để chứng thực
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        # ordering = ['-id']


class Car_card(BaseModel):
    area = models.CharField(max_length=255)


class People(BaseModel):
    name_user = models.CharField(max_length=50)
    # birthday = DateTimeField()

    def __str__(self):
        return self.name_user



