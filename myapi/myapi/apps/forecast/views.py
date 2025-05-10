from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from django.utils import timezone
from django_redis import get_redis_connection
from myapi.apps.forecast.utils import PredictionService
import json


class PredictionListView(APIView):
    def get(self, request):
        """获取最新的预测结果"""
        # 解析查询参数
        feature_name = request.query_params.get('feature')
        days = int(request.query_params.get('days', 3))
        limit = int(request.query_params.get('limit', 10))

        # 获取forecast缓存实例
        redis_conn = get_redis_connection("forecast")

        # 构建搜索模式
        if feature_name:
            pattern = f"prediction:{feature_name}:*"
        else:
            pattern = "prediction:*"

        # 获取所有匹配的键
        keys = redis_conn.keys(pattern)

        # 获取数据并过滤
        results = []
        for key in keys:
            data = redis_conn.hgetall(key)
            # 转换为字典
            data_dict = {k.decode('utf-8'): v.decode('utf-8') for k, v in data.items()}

            # 检查是否过期
            expires = datetime.fromisoformat(data_dict['expires'])
            if expires < timezone.now():
                continue

            # 检查时间范围
            generated_at = datetime.fromisoformat(data_dict['generated_at'])
            if generated_at < (timezone.now() - timedelta(days=days)):
                continue

            # 反序列化values字段
            data_dict['values'] = json.loads(data_dict['values'])

            results.append(data_dict)

        # 排序和分页
        results.sort(key=lambda x: x['generated_at'], reverse=True)
        paginated_results = results[:limit]

        return Response({
            'count': len(results),
            'results': paginated_results
        }, status=status.HTTP_200_OK)


class TriggerPredictionView(APIView):
    def periodic_prediction(self, target_indices, pipe):
        try:
            # 初始化预测服务
            predictor = PredictionService(target_indices=target_indices)
            prediction = predictor.make_prediction()

            # 获取最新数据日期
            last_date = predictor.data_loader.get_last_date()
            last_date_dt = datetime(
                year=last_date['year'],
                month=last_date['month'],
                day=last_date['day']
            )

            # 预测开始日期为最后日期的下1天
            forecast_start_date = last_date_dt + timedelta(days=1)
            # 预测结束日期为预测开始日期的后15天
            forecast_end_date = forecast_start_date + timedelta(days=14)

            feature_name = prediction['feature_name']
            # 创建唯一的键名
            key = f"prediction:{feature_name}:{forecast_start_date.strftime('%Y%m%d')}-{forecast_end_date.strftime('%Y%m%d')}"
            # 存储的数据结构
            print(timezone.now().isoformat())
            data = {
                'feature': feature_name,
                'values': json.dumps(prediction['values']),  # 序列化列表为JSON字符串
                'generated_at': timezone.now().isoformat(),
                'expires': (timezone.now() + timedelta(days=7)).isoformat()
            }
            # 存储到Redis，设置7天过期
            pipe.hset(key, mapping=data)
            pipe.expire(key, 7 * 24 * 3600)  # 7天过期


            return f"成功生成预测结果，日期：{forecast_start_date.date()}-{forecast_end_date.date()}"
        except Exception as e:
            raise Exception(f"预测任务失败: {str(e)}")

    def post(self, request):
        """手动触发预测任务"""
        target_indices = request.data.get('target_indices', [0,1,2])
        try:
            # 获取redis连接对象
            redis_conn = get_redis_connection('forecast')
            results = []
            with redis_conn.pipeline() as pipe:
                for target_index in target_indices:
                    result = self.periodic_prediction(target_index, pipe)
                    results.append(result)if target_indices else 1
                pipe.execute()

            return Response({
                'status': '任务已提交',
                'results': results
            }, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({
                'status': '任务提交失败',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


