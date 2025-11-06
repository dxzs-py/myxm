import json

from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Growth, Crop
from .serializers import GrowthSerializer
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import logging

logger = logging.getLogger("django")

class GrowthListAPIView(APIView):
    def get(self, request):
        try:
            # 1. 获取请求参数和查询数据
            request_data = request.query_params
            crop = request_data.get("crop", "葡萄")
            queryset = Growth.objects.filter(is_show=True, crop__crop_class=crop).all()
            now_date = datetime.now().date()

            # 2. 计算所有阶段的实际时间范围和状态
            stages_info = []
            active_stage = None

            for stage in queryset:
                # 构建日期对象
                start_date = datetime(now_date.year, stage.begin_time_month, stage.begin_time_day).date()
                end_date = datetime(now_date.year, stage.end_time_month, stage.end_time_day).date()

                # 处理跨年情况
                if stage.begin_time_month > stage.end_time_month:
                    if now_date >= end_date:
                        # 当前日期在今年结束日期之后，周期为今年开始，明年结束
                        start_date = datetime(now_date.year, stage.begin_time_month, stage.begin_time_day).date()
                        end_date = datetime(now_date.year + 1, stage.end_time_month, stage.end_time_day).date()
                    else:
                        # 当前日期在今年结束日期之前，周期为去年开始，今年结束
                        start_date = datetime(now_date.year - 1, stage.begin_time_month, stage.begin_time_day).date()
                        end_date = datetime(now_date.year, stage.end_time_month, stage.end_time_day).date()

                # 判断是否为当前活跃阶段
                is_current_stage = start_date <= now_date <= end_date
                if is_current_stage and active_stage is None:
                    active_stage = stage

                stages_info.append({
                    'stage': stage,
                    'start_date': start_date,
                    'end_date': end_date,
                    'is_current': is_current_stage,
                    'begin_time_month': stage.begin_time_month,
                    'begin_time_day': stage.begin_time_day
                })

            # 3. 作物生长阶段排序逻辑
            # 先按生长阶段的月份和日期排序
            stages_info.sort(key=lambda x: (x['begin_time_month'], x['begin_time_day']))
            ordered_stages = stages_info

            # 如果有活跃阶段，则确保其前后阶段正确标记
            if active_stage:
                # 找出当前活跃阶段的索引
                active_index = -1
                for i, stage_info in enumerate(ordered_stages):
                    if stage_info['stage'] == active_stage:
                        active_index = i
                        break

                # 如果找到了活跃阶段，调整数据中的标记
                if active_index != -1:
                    # 这里不需要重新排序，只需要在后续步骤中正确标记前后阶段即可
                    pass

            # 4. 序列化数据并添加标记
            ordered_stage_objects = [item['stage'] for item in ordered_stages]
            serializer = GrowthSerializer(ordered_stage_objects, many=True)
            data = serializer.data

            # 添加额外信息和标记
            current_index = -1
            for i, item in enumerate(data):
                item['in_stage'] = ordered_stages[i]['is_current']
                item['start_date'] = ordered_stages[i]['start_date'].strftime('%Y-%m-%d')
                item['end_date'] = ordered_stages[i]['end_date'].strftime('%Y-%m-%d')

                if ordered_stages[i]['is_current']:
                    item['is_current'] = True
                    current_index = i

            # 标记前一个和后一个阶段
            if current_index != -1:
                if current_index > 0:
                    data[current_index - 1]['is_previous'] = True
                if current_index < len(data) - 1:
                    data[current_index + 1]['is_next'] = True

            return Response({'code': 200, 'data': data})
        except Exception as e:
            logger.error(f"获取生长阶段列表失败: {str(e)}")
            return Response({'code': 500, 'msg': f'获取生长阶段列表失败: {str(e)}'})


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
                    "value": item.id,
                    "selected": False,
                    "image": request.build_absolute_uri(item.crop_img.url) if item.crop_img else ""
                })
        except:
            return Response({"message": "查询失败"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"crops": data}, status=status.HTTP_200_OK)
