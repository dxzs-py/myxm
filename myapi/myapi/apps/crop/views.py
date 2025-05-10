from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Growth, PlantArea
from .serializers import GrowthSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class GrowthListAPIView(ListAPIView):
    queryset = Growth.objects.filter(is_show=True).order_by("-id")
    serializer_class = GrowthSerializer


from .models import PlantArea
from myapi.settings import constants


class PlantAreaListAPIView(APIView):
    def get(self, request):
        request_data = request.query_params
        crop = request_data.get("crop", "葡萄")
        city_list = constants.CITY_LIST
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
