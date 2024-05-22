import random
import string
import yagmail
from django.db.models import Q
from rest_framework import viewsets, generics, status, parsers, permissions
from QlChungCu import serializers, paginators
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, People, CarCard, Box, Goods, Letters, Bill
from .serializers import PeopleSerializers, UserSerializers, CarCardSerializers, BoxSerializers, GoodsSerializers, \
    LettersSerializers, BillSerializers, UpdateResidentSerializer, \
    ForgotPasswordSerializers


# # ModelViewSet Kế thừa APIview, APIview kế thừa tiêu chuẩn của django
# # ModelViewSet implament 1 số thứ sẵn từ model
# # ModelViewSet chỉ cần chỉ định 2 th:  + Queryset: Câu truy vấn dựa vào đổ lên model cho mình
# #                                      + serializer: pare danh sách lấy được ở queryset ra bên ngoài, và create update, retrofit
# # ListAPIView : GET /Urlname/
# # RetrieveAPIView: GET /Urlname/{id}/
# # CreateAPIView: POST /Urlname/
# # DestroyAPIView: DELETE /Urlname/
# # UpdateAPIView: PUT + PATCH  /Urlname/{id}/
# # ListCreateAPIView: GET + POST /Urlname/
# # RetrieveUpdateAPIView: GET + PUT + PATCH /Urlname/{id}/
# # RetrieveDestroyAPIView: GET + DELETE /Urlname/{id}/
# # RetrieveUpdateDestroyAPIView: GET + PUT + PATCH + DELETE /Urlname/{id}/


# API THÔNG TIN USER RESIDENT
class ResidentLoginViewset(viewsets.ViewSet, generics.ListAPIView):  # API Người dùng đăng nhập
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializers

    def get_permissions(self):
        if self.action in ['update_acount']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    # Khi nguời dùng đăng nhập lần đầu tiên thì bắt buộc đổi mk + avt
    @action(methods=['patch'], url_path='home', detail=True)
    def update_acount(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"message": "Acount not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.change_password_required:
            # Nếu change_password_required là True, chỉ xuất ra dữ liệu của tài khoản
            serializer = UserSerializers(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Nếu update_acount là False, cho phép người dùng cập nhật pass_acount và avata_acount
        serializer = UpdateResidentSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(change_password_required=True)  # Đặt change_password_required thành True sau khi cập nhật
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Thong tin tai khoang User
    @action(methods=['get'], url_path='get_user', detail=False)  # Người dùng xem thông tin user đăng nhập của mình
    def get_user(self, request):
        # Lấy người dùng đang đăng nhập từ request
        current_user = request.user
        user = User.objects.filter(id=current_user.id).first()
        serialized = self.serializer_class(user).data
        return Response(serialized, status=status.HTTP_200_OK)
    # def get_queryset(self):
    #     queryset = self.queryset
    #
    #     q = self.request.query_params.get('q')
    #     if q:
    #         queryset = queryset.filter(name_acount__icontains=q)
    #
    #     ad_id = self.request.query_params.get('admin_id')
    #
    #     if ad_id:
    #         queryset = queryset.filter(admin_id=ad_id)
    #     return queryset


# APTI THẺ GIỮ XE
class CarCardViewset(viewsets.ViewSet, generics.ListAPIView):
    queryset = CarCard.objects.filter(is_active=True)
    serializer_class = CarCardSerializers

    def get_permissions(self):
        if self.action in ['create_carcard', ]:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='get_card', detail=True)  # Người dùng xem thông tin thẻ xe của mình
    def get_carcard(self, request, pk):
        # Lấy người dùng đang đăng nhập từ request
        current_user = request.user
        # Lấy thông tin các thẻ xe mà người dùng đã đăng ký
        carcard_user = CarCard.objects.filter(user=current_user)
        serialized_data = self.serializer_class(carcard_user, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='update_card',
            detail=False)  # Người dùng đăng ký thẻ xe cho mình hoặc người thân
    def create_carcard(self, request):
        current_user = request.user

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(user=current_user,
                            status_card=CarCard.EnumStatusCard.WAIT)  # Tạo 1 thẻ xe gán vào user đang đăng nhập
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API HÓA ĐƠN
class BillViewSet(viewsets.ViewSet, generics.ListAPIView):

    def get_permissions(self):
        if self.action in ['get_bill']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    queryset = Bill.objects.filter(is_active=True)
    serializer_class = BillSerializers

    # Xem hóa đơn của người dùng hiện có
    @action(methods=['get'], url_path='get_bill', detail=False)
    def get_bill(self, request):
        # Lấy người dùng đang đăng nhập từ request
        current_user = request.user
        # Lấy thông tin các Hóa đơn mà người dùng đang có
        bill_user = Bill.objects.filter(user_resident=current_user.id)
        serialized_data = self.serializer_class(bill_user, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)

    # Người dùng tìm kiếm hóa đơn theo tên và id
    @action(methods=['get'], url_path='search_bill', detail=True)
    def search_bill(self, request, pk):
        current_user = request.user
        bill_id = request.query_params.get('id', None)
        bill_name = request.query_params.get('name', None)

        bills = Bill.objects.filter(user_resident=current_user.id)

        if bill_id:
            bills = bills.filter(id=bill_id)
        if bill_name:
            # Sử dụng Q object để tìm kiếm theo tên bill
            bills = bills.filter(Q(name_bill__icontains=bill_name))# icontains : Tìm kiếm không phân biệt hoa thường

        serialized_data = self.serializer_class(bills, many=True).data

        if not serialized_data:  # Kiểm tra có hóa đơn nào phù hợp hay không
            return Response({"message": "No bills found with the given criteria"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialized_data, status=status.HTTP_200_OK)


# API TỦ ĐỒ
class BoxViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Box.objects.filter(is_active=True)
    serializer_class = BoxSerializers

    def get_box(self, request):
        # Lấy người dùng đang đăng nhập từ request
        current_user = request.user
        # Lấy thông tin các Hóa đơn mà người dùng đang có
        box_user = Box.objects.filter(user_resident=current_user.id)
        serialized_data = self.serializer_class(box_user, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)


#API INFO DÙNG ĐỂ XỮ LÝ QUÊN MẬT KHẨU
class InfoViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = People.objects.filter(is_active=True)
    serializer_class = ForgotPasswordSerializers

    #API tạo code xử lý quên mật khẩu
    @action(methods=['post'], url_path='create_passForgot', detail=False)
    def create_passForgot(self, request):
        name_people = request.data.get('name_people')
        identification_card = request.data.get('identification_card')

        try:
            person = People.objects.get(identification_card=identification_card, name_people=name_people)
        except People.DoesNotExist:
            return Response({"message": "Không tìm thấy người dùng"},
                            status=status.HTTP_404_NOT_FOUND)

        # Tạo mã code ngẫu nhiên
        code = ''.join(random.choices(string.digits, k=6))

        # Xử lý gửi mail
        yag = yagmail.SMTP("phanloan2711@gmail.com", 'mpgnbisxmfgwpdbg')
        to = person.user.email
        subject = 'CHUNG CƯ HIỀN VY: Mã xác thực đổi mật khẩu'
        body = f'Mã xác thực của bạn là: {code}'
        yag.send(to=to, subject=subject, contents=body)

        # Lưu mã code vào session của người dùng
        request.session['verification_code'] = code
        request.session['user_id'] = person.user.id
        request.session.modified = True  # Đảm bảo session được cập nhật

        return Response({"message": "Mã xác thực đã được gửi qua email", "code":  code}, status=status.HTTP_200_OK)


    @action(methods=['post'], url_path='reset_password', detail=False)
    def reset_password(self, request):
        code = request.data.get('code')
        new_password = request.data.get('password')
        print(new_password)

        # Lấy mã code đã lưu trong session của người dùng
        session_code = request.session.get('verification_code')
        user_id = request.session.get('user_id')

        if not session_code or not user_id:
            return Response({"message": "Session không hợp lệ hoặc đã hết hạn"}, status=status.HTTP_400_BAD_REQUEST)

        if code != session_code:
            return Response({"message": "Mã xác thực không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "Không tìm thấy người dùng"}, status=status.HTTP_404_NOT_FOUND)

        # Đặt mật khẩu mới cho người dùng
        user.set_password(new_password)
        user.change_password_required = True
        user.save()

        # Xóa mã code khỏi session sau khi đã sử dụng
        del request.session['verification_code']
        del request.session['user_id']

        return Response({"message": "Mật khẩu đã được đặt lại thành công"}, status=status.HTTP_200_OK)





# class UserResidentViewset(viewsets.ViewSet, generics.ListAPIView):
#     queryset = User.objects.filter(is_active=True, user_role ='Resident')  # Lấy các tài khoản cư dân đang active
#     serializer_class = UserSerializers
#     # Tạo 5 API:
#     # List (GET) --> Xem danh sách Tài khoản cư dan
#     # ... (POST) --> Thêm cư dân
#     # detail --> Xem chi tiết thông tin Tài khoản cư dân
#     # ... --> Cập nhập
#     # ... (DELETE) --> Xoá Tài khoản cư dân
#
#
#     # def get_permissions(self):
#     #     if self.action in ['get_acount']:
#     #         return [permissions.IsAuthenticated()]
#     #
#     #     return [permissions.AllowAny()]
#
#     #Lấy danh sach cac tai khoang cu dan ma admin do dang quan lý  /acoutAdmin/{id}/acount_get/
#     @action(methods=['get'], url_path='get_user', detail=True)
#     def get_acount(self, request, pk):
#         acount_user = User.objects.filter(is_active=True, user_role ='Resident')
#
#         return Response(serializers.UserSerializers(acount_user, many=True).data, status=status.HTTP_200_OK)
# #
# #
# #     #Tạo một tài khoảng mới cho cư dân  /acoutAdmin/{id}/acount_create/
#     @action(methods=['post'], url_path='create_user', detail=True)
#     def create_acount(self, request, pk):
#         serializer = UserSerializers(data=request.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#         # Lấy thông tin người dùng đăng nhập từ request.user
#         if request.user.is_authenticated:  # Kiểm tra xem người dùng đã đăng nhập chưa
#             admin = request.user  # Lấy thông tin admin đăng nhập
#
#             # Tạo tài khoản khách hàng với area_admin là area_admin của admin đăng nhập
#             serializer = AcountSerializers(data=request.data)
#             if serializer.is_valid():
#                 serializer.save(area_admin=admin.area_admin, admin=admin)  # Gán giá trị cho area_admin và admin
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response("User is not authenticated", status=status.HTTP_401_UNAUTHORIZED)
#
#
#
# class PeopleViewset(viewsets.ModelViewSet):
#     queryset = People.objects.filter(is_active=True)
#     serializer_class = PeopleSerializers
#     pagination_class = paginators.PeoplePaginator
#
#

#
#
# class AcountViewset(viewsets.ViewSet, generics.ListAPIView):
#     queryset = Acount.objects.filter(is_active=True)
#     serializer_class = AcountSerializers
#
#     #Khi nguời dùng đăng nhập lần đầu tiên thì bắt buộc đổi mk + avt
#     @action(methods=['put'], url_path='home', detail=True)
#     def update_acount(self, request, pk):
#         try:
#             acount = Acount.objects.get(pk=pk)
#         except Acount.DoesNotExist:
#             return Response({"message": "Acount not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         if acount.update_acount:
#             # Nếu update_acount là True, chỉ xuất ra dữ liệu của tài khoản
#             serializer = AcountSerializers(acount)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         # Nếu update_acount là False, cho phép người dùng cập nhật pass_acount và avata_acount
#         serializer = UpdateAcountSerializer(acount, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save(update_acount=True)  # Đặt update_acount thành True sau khi cập nhật
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#
#
#
#     def get_queryset(self):
#         queryset = self.queryset
#
#         q = self.request.query_params.get('q')
#         if q:
#             queryset = queryset.filter(name_acount__icontains=q)
#
#         ad_id = self.request.query_params.get('admin_id')
#
#         if ad_id:
#             queryset = queryset.filter(admin_id=ad_id)
#         return queryset
#
#
# class BoxViewset(viewsets.ModelViewSet):
#     queryset = Box.objects.filter(is_active=True)
#     serializer_class = BoxSerializers
#
#
# class GoodsViewset(viewsets.ModelViewSet):
#     queryset = Goods.objects.filter(is_active=True)
#     serializer_class = GoodsSerializers
#
#
# class LettersViewset(viewsets.ModelViewSet):
#     queryset = Letters.objects.filter(is_active=True)
#     serializer_class = LettersSerializers
#
#
# class BillViewset(viewsets.ModelViewSet):
#     queryset = Bill.objects.filter(is_active=True)
#     serializer_class = BillSerializers
#
#
#
