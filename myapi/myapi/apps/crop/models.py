from django.core.exceptions import ValidationError
from django.db import models
from myapi.utils.models import BaseModel

class Crop(BaseModel):
    crop_class = models.CharField(max_length=64, verbose_name="作物类别")
    crop_img = models.ImageField(upload_to="crop_img", null=True, blank=True, verbose_name="作物图片")

    class Meta:
        db_table = "xm_crop"
        verbose_name = "作物"
        verbose_name_plural = "作物"

    @property
    def crop_class_display(self):
        return self.crop_class

    def __str__(self):
        return self.crop_class_display


class Growth(BaseModel):
    # 模型字段
    crop = models.ForeignKey(
        "Crop",
        related_name="crop_growth",
        on_delete=models.CASCADE,
        verbose_name="作物",
    )
    growth_cycle = models.CharField(max_length=64, verbose_name="成长周期", blank=True, null=True)
    begin_time = models.DateField(verbose_name="开始日期", blank=True, null=True)
    end_time = models.DateField(verbose_name="结束日期", blank=True, null=True)
    growth_temp_min = models.FloatField(verbose_name="最低适宜温度(℃)", blank=True, null=True)
    growth_temp_max = models.FloatField(verbose_name="最高适宜温度(℃)", blank=True, null=True)
    growth_humidity_min = models.FloatField(verbose_name="最低适宜湿度(%)", blank=True, null=True)
    growth_humidity_max = models.FloatField(verbose_name="最高适宜湿度(%)", blank=True, null=True)
    growth_rainfall_min = models.FloatField(verbose_name="最低适宜降雨量(mm)", blank=True, null=True)
    growth_rainfall_max = models.FloatField(verbose_name="最高适宜降雨量(mm)", blank=True, null=True)
    growth_wind_min = models.FloatField(verbose_name="最低适宜风速(m/s)", blank=True, null=True)
    growth_wind_max = models.FloatField(verbose_name="最高适宜风速(m/s)", blank=True, null=True)
    sunshine_hours_min = models.FloatField(verbose_name="最短日照时长(h)", blank=True, null=True)
    sunshine_hours_max = models.FloatField(verbose_name="最长日照时长(h)", blank=True, null=True)

    class Meta:
        db_table = "xm_crop_growth"
        verbose_name = "该生长周期的作物适宜条件"
        verbose_name_plural = "该生长周期的作物适宜条件"

    def __str__(self):
        return f"{self.begin_time} - {self.crop} - {self.end_time}"

    def clean(self):
        # 添加数据验证
        if self.growth_temp_min is not None and self.growth_temp_max is not None:
            if self.growth_temp_min > self.growth_temp_max:
                raise ValidationError("最低适宜温度不能高于最高适宜温度")

        if self.growth_humidity_min is not None and self.growth_humidity_max is not None:
            if self.growth_humidity_min > self.growth_humidity_max:
                raise ValidationError("最低适宜湿度不能高于最高适宜湿度")

        if self.growth_rainfall_min is not None and self.growth_rainfall_max is not None:
            if self.growth_rainfall_min > self.growth_rainfall_max:
                raise ValidationError("最低适宜降雨量不能高于最高适宜降雨量")

        if self.growth_wind_min is not None and self.growth_wind_max is not None:
            if self.growth_wind_min > self.growth_wind_max:
                raise ValidationError("最低适宜风速不能高于最高适宜风速")

        if self.sunshine_hours_min is not None and self.sunshine_hours_max is not None:
            if self.sunshine_hours_min > self.sunshine_hours_max:
                raise ValidationError("最短日照时长不能高于最长日照时长")



class PlantArea(BaseModel):
    crop = models.ForeignKey(
        "Crop",
        related_name="crop_plant",
        on_delete=models.CASCADE,
        verbose_name="种植作物",
    )
    city = models.ForeignKey(
        "user.City",
        related_name="city_plant",
        on_delete=models.PROTECT,
        verbose_name="城市",
    )
    name = models.CharField(max_length=64, verbose_name="名称", default="")
    including_areas = models.CharField(max_length=64, verbose_name="包含的种植区域", default="")
    longitude = models.FloatField(verbose_name="经度")
    latitude = models.FloatField(verbose_name="纬度")
    area = models.FloatField(verbose_name="面积(万亩)")

    class Meta:
        db_table = "xm_plant_area"
        verbose_name = "种植区"
        verbose_name_plural = "种植区"
        unique_together = ('crop', 'city', 'longitude', 'latitude')

    def __str__(self):
        return f"{self.city} - {self.crop}"

    def clean(self):
        # 验证经纬度范围
        if self.longitude < -180 or self.longitude > 180:
            raise ValidationError("经度必须在-180到180之间")
        if self.latitude < -90 or self.latitude > 90:
            raise ValidationError("纬度必须在-90到90之间")
        if self.area <= 0:
            raise ValidationError("面积必须为正数")


"""
# 删除所有应用的迁移文件
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# 然后重新生成迁移文件
python manage.py makemigrations
python manage.py migrate
"""