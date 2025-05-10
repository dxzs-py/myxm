from django.apps import AppConfig
from celery import Celery


class WeatherPredictionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forecast'
    verbose_name = '气象预测'