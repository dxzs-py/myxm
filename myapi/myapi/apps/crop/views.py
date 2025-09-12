from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Growth,Crop
from .serializers import GrowthSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class GrowthListAPIView(ListAPIView):
    queryset = Growth.objects.filter(is_show=True).order_by("-id")
    serializer_class = GrowthSerializer


from .models import PlantArea
from myapi.settings import constants
from user.models import City

class PlantAreaListAPIView(APIView):
    def get(self, request):
        request_data = request.query_params
        crop = request_data.get("crop", "葡萄")
        city_list = City.objects.filter(is_show=True).values_list("name", flat=True)
        """
        .values_list("name", flat=True) - 以列表形式返回查询结果，且只包含name字段的值
        当flat=True时，结果会是['北京', '上海', '广州']这样的平铺列表
        如果flat=False（默认），结果会是[('北京',), ('上海',), ('广州',)]这样的元组列表
        """
        data = []
        try:
            for city in city_list:
                mes = PlantArea.objects.filter(city__name=city, crop__crop_class=crop, is_show=True).order_by("-id")
                detail = {
                    "city": city,
                    "value": []
                }
                for item in mes:
                    detail["value"].append({
                        "name": item.name,
                        "value": [item.longitude, item.latitude, item.area]
                    })
                data.append(detail)
        except:
            return Response({"message": "查询失败"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"productionArea": data}, status=status.HTTP_200_OK)

from .models import Crop

class CropListAPIView(APIView):
    def get(self, request):
        data = []
        try:
            crop_class = Crop.objects.filter(is_show=True).order_by("-id")
            for item in crop_class:
                data.append({
                    "name": item.crop_class,
                    "value":item.id,
                    "selected":False,
                    "image": request.build_absolute_uri(item.crop_img.url) if item.crop_img else ""
                })
        except:
            return Response({"message": "查询失败"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"crops": data}, status=status.HTTP_200_OK)