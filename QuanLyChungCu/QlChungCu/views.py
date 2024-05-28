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
from datetime import datetime, timedelta, timezone, time
from django.views.decorators.csrf import csrf_exempt
import json
import urllib.request
import urllib
import uuid
import requests
import hmac
import hashlib
from django.http import HttpResponse, JsonResponse


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


# API THẺ GIỮ XE
class CarCardViewset(viewsets.ViewSet, generics.ListAPIView):
    queryset = CarCard.objects.filter(is_active=True)
    serializer_class = CarCardSerializers

    def get_permissions(self):
        if self.action in ['create_carcard', 'delete_card']:
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

    @action(methods=['post'], url_path='update_card', detail=False)
    def create_carcard(self, request):
        current_user = request.user

        # Kiểm tra số lượng thẻ xe của người dùng
        num_carcards = CarCard.objects.filter(user=current_user).count()
        if num_carcards >= 3:
            return Response({"error": "Bạn đã đạt tối đa số lượng thẻ xe."},
                            status=status.HTTP_403_FORBIDDEN)  # từ chối

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(user=current_user,
                            status_card=CarCard.EnumStatusCard.CONFIRMER, is_active=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # API Xóa thẻ xe

    @action(methods=['delete'], url_path='delete_card', detail=False)
    def delete(self, request):
        current_user = request.user
        carcard_data = request.data
        carcard_id = carcard_data.get('id')
        try:
            carcard = CarCard.objects.get(user=current_user, id=carcard_id)
        except CarCard.DoesNotExist:
            return Response({"error": "Không tìm thấy thẻ xe hoặc thẻ xe không thuộc về người dùng hiện tại!"},
                            status=status.HTTP_404_NOT_FOUND)

        carcard.delete()
        return Response({"message": "Thẻ xe đã được xóa thành công."}, status=status.HTTP_200_OK)

# # API HÓA ĐƠN
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
            bills = bills.filter(Q(name_bill__icontains=bill_name))  # icontains : Tìm kiếm không phân biệt hoa thường

        serialized_data = self.serializer_class(bills, many=True).data

        if not serialized_data:  # Kiểm tra có hóa đơn nào phù hợp hay không
            return Response({"message": "No bills found with the given criteria"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialized_data, status=status.HTTP_200_OK)


# API TỦ ĐỒ
class BoxViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Box.objects.filter(is_active=True)
    serializer_class = BoxSerializers

    @action(methods=['get'], url_path='get_box', detail=False)
    def get_box(self, request):
        # Lấy người dùng đang đăng nhập từ request
        current_user = request.user
        # Lấy thông tin các Hóa đơn mà người dùng đang có
        box_user = Box.objects.filter(user_admin=current_user.id)
        serialized_data = self.serializer_class(box_user, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)



class GoodsViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Goods.objects.filter(is_active=True)
    serializer_class = GoodsSerializers

    @action(methods=['get'], url_path='get_goods', detail=False)
    def get_goods(self, request):
        try:
            box_id = request.data.get('id')  # Sử dụng query_params thay vì data
            goods_data = Goods.objects.filter(box=box_id)
            serialized_data = GoodsSerializers(goods_data, many=True).data
            return Response(serialized_data, status=status.HTTP_200_OK)
        except Goods.DoesNotExist:
            return Response({"message": "Không tìm thấy thông tin hàng hóa"}, status=status.HTTP_404_NOT_FOUND)


# API INFO NGUOI DUNG
class InfoViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = People.objects.filter(is_active=True)
    serializer_class = ForgotPasswordSerializers

    # API tạo code xử lý quên mật khẩu
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

        return Response({"message": "Mã xác thực đã được gửi qua email", "code": code}, status=status.HTTP_200_OK)

    #API gui mat khau moi
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
        user.password = new_password
        # user.set_password(new_password)
        user.change_password_required = True
        user.save()

        # Xóa mã code khỏi session sau khi đã sử dụng
        del request.session['verification_code']
        del request.session['user_id']

        return Response({"message": "Mật khẩu đã được đặt lại thành công"}, status=status.HTTP_200_OK)




class InfoPeopleViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = People.objects.filter(is_active=True)
    serializer_class = PeopleSerializers

    @action(methods=['get'], url_path='get_infopeople', detail=False)
    def get_infopeople(self, request):
        # Lấy người dùng đăng nhập hiện tại
        user = request.user
        try:
            # Tìm thông tin People tương ứng với người dùng
            people_data = People.objects.get(user=user)
        except People.DoesNotExist:
            return Response({"message": "Không tìm thấy thông tin người dùng"}, status=status.HTTP_404_NOT_FOUND)

        serialized_data = self.serializer_class(people_data).data
        return Response(serialized_data, status=status.HTTP_200_OK)


# API MOMO
class MomoViewSet(viewsets.ViewSet):
    serializer_class = BillSerializers

    # Hứng Data từ momo gửi về
    @action(detail=False, methods=['post'], url_path='momoipn')
    @csrf_exempt
    def momo_ipn(self, request):
        try:
            payment_data = request.data
            print(payment_data)
            result_code = payment_data.get("resultCode")
            orderInfo = payment_data.get('orderInfo')  # Trường orderInfo chứa id của cái Bill.
            print(orderInfo)
            orderId = payment_data.get('orderId')
            amount = payment_data.get('amount')
            print(amount)

            if result_code != 0:
                return JsonResponse({'error': "Thanh toán thất bại", 'status': 400})

            # Tìm tất cả các Bill thỏa mãn điều kiện id=orderInfo, money=amount
            bills = Bill.objects.filter(id=orderInfo, money=amount)

            # Kiểm tra nếu không có Bill thỏa mãn điều kiện, trả về lỗi
            if not bills.exists():
                return Response({"error": "Không tìm thấy hóa đơn tương ứng", 'status': status.HTTP_404_NOT_FOUND})

            # Thay đổi trạng thái của tất cả các Bill thỏa mãn điều kiện thành "paid"
            print('Tới update')
            bills.update(status_bill=Bill.EnumStatusBill.PAID, trading_code=orderId, payment_style='Momo')

            return Response({"message": "Thành công"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'error': str(e)})

    @action(detail=False, methods=['post'], url_path='create', url_name='momo_create')
    @csrf_exempt
    def create_momo_payment(self, request):

        endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
        ipnUrl = "https://7a7f-171-243-48-141.ngrok-free.app/momo/momoipn/"

        accessKey = "F8BBA842ECF85"
        secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
        partnerCode = "MOMO"
        orderInfo = self.request.data.get('id')
        requestId = str(uuid.uuid4())
        amount = self.request.data.get('total')
        orderId = str(uuid.uuid4())
        # orderId = total.get('appointment_id')+total.get('user_id')+total.get('booking_date')

        requestType = "captureWallet"
        extraData = ""
        redirectUrl = ""

        rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl \
                       + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode \
                       + "&redirectUrl=" + redirectUrl + "&requestId=" + requestId + "&requestType=" + requestType

        h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
        signature = h.hexdigest()
        data = {
            'partnerCode': partnerCode,
            'partnerName': "Test",
            'storeId': "MomoTestStore",
            'requestId': requestId,
            'amount': amount,
            'orderId': orderId,
            'orderInfo': orderInfo,
            'redirectUrl': redirectUrl,
            'ipnUrl': ipnUrl,
            'lang': "vi",
            'extraData': extraData,
            'requestType': requestType,
            'signature': signature,
            'orderExpireTime': 10,
        }

        data = json.dumps(data)

        clen = len(data)
        response = requests.post(endpoint,
                                 data=data,
                                 headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})

        if response.status_code == 200:
            response_data = response.json()
            return JsonResponse({**response_data})
        else:
            return JsonResponse({'error': 'Invalid request method'})


# API ZALO
class ZaloViewSet(viewsets.ViewSet):
    serializer_class = BillSerializers

    @csrf_exempt
    @action(detail=False, methods=['post'], url_path='create', url_name='create_zalo')
    def create_zalo_payment(self, request):  # tạo đường link thanh toán
        endpoint = "https://sb-openapi.zalopay.vn/v2/create"
        app_id = 2553
        key1 = "PcY4iZIKFCIdgZvA6ueMcMHHUbRLYjPL"
        key2 = "kLtgPl8HHhfvMuDHPwKfgfsY4Ydm9eIz"

        appuser = self.request.data.get('id')
        transID = random.randrange(1000000)
        apptime = int(round(datetime.now().timestamp() * 1000))  # milliseconds
        app_trans_id = "{:%y%m%d}_{}".format(datetime.today(), transID)
        print("t", app_trans_id)
        embed_data = json.dumps({})
        item = json.dumps([{}])
        amount = self.request.data.get('amount')
        callback_url = 'https://7a7f-171-243-48-141.ngrok-free.app/zalo/query_zalopay/'

        # Tạo chuỗi dữ liệu theo định dạng yêu cầu
        raw_data = "{}|{}|{}|{}|{}|{}|{}".format(app_id, app_trans_id, appuser, amount, apptime, embed_data, item)

        # Tính toán MAC bằng cách sử dụng HMAC
        mac = hmac.new(key1.encode(), raw_data.encode(), hashlib.sha256).hexdigest()
        print("mac trong API Gửi" + mac)

        # Dữ liệu gửi đi
        data = {
            "app_id": app_id,
            "app_user": appuser,
            "app_time": apptime,
            "amount": amount,
            "app_trans_id": app_trans_id,
            "embed_data": embed_data,
            "item": item,
            "description": "Lazada - Payment for the order #" + str(transID),
            "bank_code": "zalopayapp",
            "mac": mac,
            "callback_url": callback_url
        }

        # Gửi yêu cầu tạo
        response = requests.post(url=endpoint, data=data)

        if response.status_code == 200:
            response_data = response.json()
            print(response_data)
            return JsonResponse(
                {'ok': '200', 'app_trans_id': app_trans_id, 'order_url': response_data.get('order_url')})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)

    # API hứng dữ liệu ZaLopay gửi về
    @csrf_exempt
    @action(detail=False, methods=['post'], url_path='query_zalopay', url_name='query_zalo')
    def query_zalo_payment(self, request):  # kiểm tra trạng thái thanh toán?
        result = {}
        key2 = 'kLtgPl8HHhfvMuDHPwKfgfsY4Ydm9eIz'
        try:
            cbdata = request.data
            mac = hmac.new(key2.encode(), cbdata['data'].encode(), hashlib.sha256).hexdigest()
            print("cbdata['mac'] " + cbdata['mac'])
            print(mac)
            # kiểm tra callback hợp lệ (đến từ ZaloPay server)
            if mac != cbdata['mac']:
                # callback không hợp lệ
                result['return_code'] = -1
                result['return_message'] = 'mac not equal'
            else:
                # Thanh toán thành công
                # Merchant cập nhật trạng thái cho đơn hàng
                dataJson = json.loads(cbdata['data'])
                print(f'datajson: {dataJson}')

                result['return_code'] = 1
                result['return_message'] = 'success'

                app_user = dataJson.get('app_user')  # Trường orderInfo chứa id của cái Bill.
                print(app_user)
                amount = dataJson.get('amount')
                print(amount)
                zp_trans_id = dataJson.get('zp_trans_id')
                print("thành công")
                # Tìm tất cả các Bill thỏa mãn điều kiện id=orderInfo, money=amount
                bills = Bill.objects.filter(id=app_user, money=amount)
                print("Bill : " + str(bills))  # Chuyển đổi bills thành chuỗi trước khi nối

                # Kiểm tra nếu không có Bill thỏa mãn điều kiện, trả về lỗi
                if not bills.exists():
                    return Response({"error": "Không tìm thấy hóa đơn tương ứng", 'status': status.HTTP_404_NOT_FOUND})

                # Thay đổi trạng thái của tất cả các Bill thỏa mãn điều kiện thành "paid"
                print('Tới update')
                bills.update(status_bill=Bill.EnumStatusBill.PAID, trading_code = zp_trans_id, payment_style='ZaloPay')

        except Exception as e:
            result['return_code'] = 0  # ZaloPay server sẽ callback lại (tối đa 3 lần)
            result['return_message'] = str(e)

        # Thông báo kết quả cho ZaloPay server
        print(result)
        return JsonResponse(result)
