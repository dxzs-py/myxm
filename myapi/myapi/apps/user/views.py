from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from rest_framework.pagination import PageNumberPagination
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from crop.models import Crop


class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer  # 只需修改其序列化器为刚刚自定义的即可


from myapi.libs.geetest import GeetestLib
from .serializers import get_account_by_mobile
from rest_framework import status as http_status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, get_object_or_404

# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "6386fee5f38474b4d6bb30209dfbcde3"
pc_geetest_key = "9aa2e3aec4b8e94e4145926a07d58a91"


class CaptchaAPIView(APIView):
    """验证视图类"""
    status = False
    user_id = None

    def get(self, request):
        """获取验证码"""
        username = request.query_params.get("username")
        user = get_account_by_mobile(username)
        if user is None:
            return Response({"message": "对不起，用户不存在！"}, status=http_status.HTTP_400_BAD_REQUEST)
        self.user_id = user.id
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        # todo 后面增加status和user_id保存到redis数据库中
        response_str = gt.get_response_str()
        return Response(response_str)  # 返回验证码但是是字符串类型，需要转成json类型，在客户端实现

    def post(self, request):
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        if self.status:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)


from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserModelSerializer


class UserAPIView(CreateAPIView):
    """用户信息视图"""
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


import re

"""
GET /user/mobile/<mobile>/
"""


class MobileAPIView(APIView):
    """手机号验证视图"""

    def get(self, request, mobile):
        # 验证手机号是否已经被注释过了
        if re.search("/", mobile):
            mobile = mobile.replace("/", "")
        reg = get_account_by_mobile(mobile)
        if reg is not None:
            return Response({"message": "手机号已经被注册"}, status=http_status.HTTP_400_BAD_REQUEST)
        return Response({"message": "改手机号未被注册，可以进行注册"}, status=http_status.HTTP_200_OK)


import random
from django_redis import get_redis_connection
from myapi.settings import constants
from myapi.libs.yuntongxun.sms import CCP


class SmSAPIView(APIView):
    """短信验证码视图"""

    def get(self, request, mobile):
        """短信发送"""
        # todo 1.判断手机号是否在60秒内曾经发送过短信
        if re.search("/", mobile):
            mobile = mobile.replace("/", "")
        redis_conn = get_redis_connection("sms_code")
        ret = redis_conn.get("mobile_%s" % mobile)
        if ret is not None:
            return Response({"message": "短信60秒内发送过，请耐心等待"}, status=http_status.HTTP_400_BAD_REQUEST)

        # 2.生成短信验证码
        sms_code = "%04d" % random.randint(1000, 9999)  # 方案1
        # sms_code = f"{random.randint(100000, 999999):06}"  # 方案2
        # sms_code = "{:06}".format(random.randint(100000, 999999))  # 方案3

        # 3.保存短信验证码到redis数据库中
        # redis_conn = get_redis_connection("sms_code")
        redis_conn.setex("sms_%s" % mobile, constants.SMS_EXPIRE_TIME, sms_code)
        redis_conn.setex("mobile_%s" % mobile, constants.SMS_INTERVAL_TIME, "_")

        # 4.调用短信sdk,发送短信验证码
        try:
            ccp = CCP()
            print(mobile)
            dx = ccp.send_template_sms(mobile, [str(sms_code), str(constants.SMS_EXPIRE_TIME // 60)],
                                       constants.SMS_TEMPLATE_ID)
            print(dx)
        except:
            return Response({"message": "短信发送失败"}, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 5.响应发送短信的结果
        return Response({"message": "短信发送成功"}, status=http_status.HTTP_200_OK)


from .serializers import SelfModelSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db import transaction, IntegrityError
import logging

logger = logging.getLogger("django")


class SelfAPIView(APIView):
    """用户信息视图"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 获取当前登录用户
        queryset = User.objects.all()
        user_id = self.request.user.id
        return queryset.filter(id=user_id)

    def get(self, request):
        queryset = self.get_queryset()
        serializer = SelfModelSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        user_id = request.user.id
        crops_ids = request.data.get("selectedCrops", [])
        area_ids = request.data.get("selectedArea")
        avatar = request.data.get("avatar")

        # 校验地区数据完整性
        if not area_ids or len(area_ids) != 3:
            raise ValidationError("请选择完整的省-市-县三级地区")
        province_id, city_id, county_id = area_ids

        # 获取关联对象
        city = get_object_or_404(City, id=city_id)
        county = get_object_or_404(County, id=county_id)
        # 获取用户实例
        user = get_object_or_404(User, id=user_id)
        """# 等价功能写法
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("用户不存在")
        """
        # 验证县-市关联
        if county.city_belong != city:
            raise ValidationError("所选县不属于指定城市")

        try:
            with transaction.atomic():
                # 更新字段
                if avatar and avatar != str(user.avatar):
                    user.avatar = avatar
                user.city = city
                user.county = county
                # 更新用户信息
                user.save()
                # 更新关注作物
                if isinstance(crops_ids, list):
                    crops = Crop.objects.filter(id__in=crops_ids)
                    # user.crops_interest = [1,2,3]  # ❌ 错误：不能直接赋值ID列表
                    user.crops_interest.set(crops)
                else:
                    user.crops_interest.clear()
            return Response({"message": "用户信息更新成功"}, status=200)
        except IntegrityError as e:
            logger.error(f"数据完整性错误: {str(e)}")
            return Response({"error": "数据完整性错误"}, status=400)
        except Exception as e:
            logger.error(f"用户更新失败: {str(e)}")
            return Response({"error": "内部服务器错误"}, status=500)


from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Province, City, County
from .serializers import ProvinceSerializer, CitySerializer, CountySerializer


@method_decorator(cache_page(60 * 15), name='dispatch')  # 缓存15分钟
class ProvinceListView(ListAPIView):
    """
    获取省份列表
    返回所有可用的省份信息，用于行政区划三级联动选择
    """
    queryset = Province.objects.filter(is_show=True)  # 假设使用is_show字段控制显示
    serializer_class = ProvinceSerializer
    # permission_classes = [IsAuthenticated]


class ProvinceCityListView(ListAPIView):
    """
    获取指定省份下的所有城市
    示例请求：/provinces/1/cities/
    """
    serializer_class = CitySerializer

    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            province_id = int(self.kwargs['province_id'])
        except (ValueError, TypeError):
            raise NotFound("省份ID必须为有效数字")

        if not Province.objects.filter(id=province_id).exists():
            raise NotFound("指定的省份不存在")

        return City.objects.select_related('province').filter(
            province_id=province_id
        )


class CityCountyListView(ListAPIView):
    """
    获取指定城市下的所有县区
    示例请求：/cities/10/counties/
    """
    serializer_class = CountySerializer

    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            city_id = int(self.kwargs['city_id'])
        except (ValueError, TypeError):
            raise NotFound("城市ID必须为有效数字")

        if not City.objects.filter(id=city_id).exists():
            raise NotFound("指定的城市不存在")

        return County.objects.select_related('city_belong').filter(
            city_belong_id=city_id
        )


# ... existing code ...

from rest_framework.response import Response
from .models import Province, City, County


class AreaHierarchyView(APIView):  # ✅ 使用class定义类视图
    """
    返回省市区三级联动层级结构数据
    示例结构：
    [
      {
        "id": "1",
        "name": "宁夏回族自治区",
        "children": [
          {
            "id": "2",
            "name": "银川市",
            "children": [
              {"id": "640105", "name": "西夏区"},
              {"id": "640121", "name": "永宁县"}
            ]
          }
        ]
      }
    ]
    """

    def get(self, request):  # ✅ 添加get方法
        # 获取所有省份并预取关联城市
        provinces = Province.objects.prefetch_related(
            'province_city__city_county'
        ).filter(is_show=True)

        hierarchy_data = []

        for province in provinces:
            province_data = {
                'id': str(province.id),
                'name': province.name,
                'children': []
            }

            # 获取当前省份下的所有城市
            cities = province.province_city.all()

            for city in cities:
                city_data = {
                    'id': str(city.id),
                    'name': city.name,
                    'children': []
                }

                # 获取当前城市下的所有县区
                counties = city.city_county.all()

                for county in counties:
                    city_data['children'].append({
                        'id': str(county.id),
                        'name': county.name
                    })

                province_data['children'].append(city_data)

            hierarchy_data.append(province_data)

        return Response(hierarchy_data)
