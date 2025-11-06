from rest_framework import serializers
from .models import Growth, Crop, PlantArea


class GrowthSerializer(serializers.ModelSerializer):
    """作物生长周期数据的序列化器"""

    class Meta:
        model = Growth
        fields = ["id", "crop","growth_cycle"]



