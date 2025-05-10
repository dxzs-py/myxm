# from my_celery.main import app
# from django.utils import timezone
# from datetime import datetime, timedelta
# from django_redis import get_redis_connection
# from myapi.apps.forecast.utils import PredictionService
#
#
# @app.task(
#     name='periodic_prediction_task',
#     bind=True,
#     autoretry_for=(Exception,),
#     retry_kwargs={'max_retries': 3},
#     retry_backoff=300,
#     retry_jitter=True
# )
# def periodic_prediction_task(self):
#     try:
#         # 初始化预测服务
#         predictor = PredictionService()
#         predictions = predictor.make_prediction()
#
#         # 获取最新数据日期
#         last_date = predictor.data_loader.get_last_date()
#         last_date_dt = datetime(
#             year=last_date['year'],
#             month=last_date['month'],
#             day=last_date['day']
#         )
#
#         # 预测开始日期为最后日期的下一天
#         forecast_start_date = last_date_dt + timedelta(days=1)
#
#         # 获取redis连接对象
#         redis_conn = get_redis_connection('forecast')
#
#         try:
#             with redis_conn.pipeline() as pipe:
#                 pipe.multi()
#                 for pred in predictions:
#                     feature_name = pred['feature_name']
#                     # 创建唯一的键名
#                     key = f"prediction:{feature_name}:{forecast_start_date.strftime('%Y%m%d')}"
#
#                     # 存储的数据结构
#                     data = {
#                         'feature': feature_name,
#                         'forecast_start': forecast_start_date.isoformat(),
#                         'generated_at': timezone.now().isoformat(),
#                         'values': pred['values'],
#                         'expires': (timezone.now() + timedelta(days=7)).isoformat()
#                     }
#
#                     # 存储到Redis，设置7天过期
#                     pipe.hset(key, mapping=data)
#                     pipe.expire(key, 7 * 24 * 3600)  # 7天过期
#                 pipe.execute()
#
#             return f"成功生成预测结果，开始日期：{forecast_start_date.date()}"
#         except Exception as e:
#             return f"预测任务失败: {str(e)}"
#
#     except Exception as e:
#         return f"预测任务失败: {str(e)}"
