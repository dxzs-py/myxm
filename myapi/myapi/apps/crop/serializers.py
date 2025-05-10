from rest_framework import serializers
from .models import Crop

class CropSerializer(serializers.ModelSerializer):
    """气象数据的序列化器"""
    class Meta:
        model = Crop
        fields = ["city", "begin_time", "end_time", "city_type", "growth_cycle"]