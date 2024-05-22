# serializers chuyển dữ liệu phức tạp từ Queryset thành kiểu dữ liệu đơn gian như Json để chuyển ra bên ngoài
# Có nhiều cách khai báo serializer: + Không cần model
#                                   + liên kết với model: ở đây sử dụng cách này

from QlChungCu.models import People, User, CarCard, Box, Goods, Letters, Bill
from rest_framework import serializers
import random
import string
import smtplib
from email.mime.text import MIMEText

class PeopleSerializers(serializers.ModelSerializer):
    class Meta:
        model = People
        # filter chỉ định các trường serialize ra pare thành json để gửi ra bên ngoài để client gọi API
        fields = '__all__'


class CarCardSerializers(serializers.ModelSerializer):
    class Meta:
        model = CarCard
        # filter chỉ định các trường serialize ra pare thành json để gửi ra bên ngoài để client gọi API
        fields = '__all__'


class UserSerializers(serializers.ModelSerializer):

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['avatar_acount'] = instance.avatar_acount.url

        return rep

    class Meta:
        model = User
        # filter chỉ định các trường serialize ra pare thành json để gửi ra bên ngoài để client gọi API
        fields = ['id', 'username', 'password', 'avatar_acount', 'change_password_required', ]


#         extra_kwargs = {# các trường chí ghi chớ không đọc
#                 'pass_acount': {
#                     'write_only': 'True'
#                 },
#                 'admin': {
#                     'write_only': 'True'
#                 }
#         }

class UpdateResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'avatar_acount', ]
        extra_kwargs = {
            'pass_acount': {
                'write_only': True
            }
        }


class BoxSerializers(serializers.ModelSerializer):
    class Meta:
        model = Box
        # filter chỉ định các trường serialize ra pare thành json để gửi ra bên ngoài để client gọi API
        fields = ['id', 'stand', 'describe', 'box_status',]


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
        fields = ['id', 'name_bill', 'money', 'decription', 'type_bill', 'status_bill', 'user_resident', 'created_date',
                  'updated_date', ]


class ForgotPasswordSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = People
        fields = ['name_people', 'email','identification_card']

    # def to_representation(self, instance):
    #     email_user = self.fields['email'].get_attribute(instance)  # Lấy giá trị của trường email từ đối tượng instance
    #     representation = super().to_representation(instance)
    #     code_value = ''.join(random.choices(string.digits, k=6))  # Tạo chuỗi số ngẫu nhiên gồm 6 ký tự
    #     representation['code'] = code_value  # Lưu dữ liệu trường code vào biến tạm
    #     #Xữ lý gửi mail
    #     import yagmail
    #     yag = yagmail.SMTP("phanloan2711@gmail.com", 'mpgnbisxmfgwpdbg')
    #     to = email_user
    #     subject = 'CHUNG CƯ HIỀN VY: Mã xác thực đổi mật khẩu'
    #     body = f'Mã xác thực của bạn là: {code_value}'
    #     yag.send(to=to, subject=subject, contents=body)
    #     return representation




# class CodeForgotPasswordSer(serializers.ModelSerializer):
#     fields = ['code']
#     def to_representation(self, instance):
#         email_user = self.fields['email'].get_attribute(instance)  # Lấy giá trị của trường email từ đối tượng instance
#         representation = super().to_representation(instance)
#         code_value = ''.join(random.choices(string.digits, k=6))  # Tạo chuỗi số ngẫu nhiên gồm 6 ký tự
#         representation['code'] = code_value  # Lưu dữ liệu trường code vào biến tạm
#         #Xữ lý gửi mail
#         import yagmail
#         yag = yagmail.SMTP("phanloan2711@gmail.com", 'mpgnbisxmfgwpdbg')
#         to = email_user
#         subject = 'CHUNG CƯ HIỀN VY: Mã xác thực đổi mật khẩu'
#         body = f'Mã xác thực của bạn là: {code_value}'
#         yag.send(to=to, subject=subject, contents=body)
#         return representation
#
