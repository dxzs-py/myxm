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
        verbose_name="作物"
    )
    growth_cycle = models.CharField(max_length=64, verbose_name="成长周期", blank=True, null=True)

    # 日期字段重构为月份+日号
    begin_time_month = models.IntegerField(
        choices=[(i, i) for i in range(1, 13)],
        blank=True,
        null=True,
        verbose_name="开始日期的月份"
    )
    begin_time_day = models.IntegerField(
        choices=[(i, i) for i in range(1, 32)],
        blank=True,
        null=True,
        verbose_name="开始日期的日号"
    )
    end_time_month = models.IntegerField(
        choices=[(i, i) for i in range(1, 13)],
        blank=True,
        null=True,
        verbose_name="结束日期的月份"
    )
    end_time_day = models.IntegerField(
        choices=[(i, i) for i in range(1, 32)],
        blank=True,
        null=True,
        verbose_name="结束日期的日号"
    )
    measures_precautions = models.TextField(verbose_name="关键管理措施/注意事项", blank=True, null=True)
    disasters = models.TextField(verbose_name="可能受到的灾难", blank=True, null=True)
    growth_temp = models.FloatField(verbose_name="最短适宜温度(℃)", blank=True, null=True)
    growth_temp_min = models.FloatField(verbose_name="适宜最低温度(℃)", blank=True, null=True)
    growth_temp_max = models.FloatField(verbose_name="适宜最高温度(℃)", blank=True, null=True)
    growth_humidity_min = models.FloatField(verbose_name="适宜最低湿度(%)", blank=True, null=True)
    growth_humidity_max = models.FloatField(verbose_name="适宜最高湿度(%)", blank=True, null=True)
    growth_rainfall_min = models.FloatField(verbose_name="适宜最低降雨量(mm)", blank=True, null=True)
    growth_rainfall_max = models.FloatField(verbose_name="适宜最高降雨量(mm)", blank=True, null=True)
    growth_wind_min = models.FloatField(verbose_name="适宜最低风速(m/s)", blank=True, null=True)
    growth_wind_max = models.FloatField(verbose_name="适宜最高风速(m/s)", blank=True, null=True)
    sunshine_hours_min = models.FloatField(verbose_name="最短日照时长(h)", blank=True, null=True)
    sunshine_hours_max = models.FloatField(verbose_name="最长日照时长(h)", blank=True, null=True)
    cycle_order = models.PositiveSmallIntegerField(verbose_name="生长顺序", blank=True, null=True,
                                                   help_text="用于标识生长阶段的先后顺序")
    duration_days = models.PositiveSmallIntegerField(verbose_name="大致持续天数", blank=True, null=True)
    is_critical = models.BooleanField(default=False, verbose_name="关键物候期",
                                      help_text="此时期对环境条件敏感，需特别关注")
    phenophase_code = models.CharField(max_length=20, verbose_name="物候期编码", blank=True, null=True,
                                       help_text="可参照农业标准物候期编码")

    class Meta:
        db_table = "xm_crop_growth"
        verbose_name = "该生长周期的作物适宜条件"
        verbose_name_plural = verbose_name
        ordering = ["crop", "cycle_order"]  # 建议按照作物和生长顺序默认排序

    def __str__(self):
        return f"{self.begin_time_month+self.begin_time_day} - {self.crop} - {self.end_time_month+self.end_time_day}"

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

        # 验证开始日期的合法性
        if self.begin_time_month is not None and self.begin_time_day is not None:
            if self.begin_time_month < 1 or self.begin_time_month > 12:
                raise ValidationError("开始月份必须在1到12之间")
            if self.begin_time_day < 1 or self.begin_time_day > 31:
                raise ValidationError("开始日号必须在1到31之间")

            # 根据月份判断天数是否合法
            month = self.begin_time_month
            day = self.begin_time_day

            if month in [4, 6, 9, 11] and day > 30:
                raise ValidationError(f"开始日期的月份 {month} 的日期不能超过30天")
            elif month == 2 and day > 28:
                raise ValidationError("开始日期的2月日期不能超过28天")

        # 验证结束日期的合法性
        if self.end_time_month is not None and self.end_time_day is not None:
            if self.end_time_month < 1 or self.end_time_month > 12:
                raise ValidationError("结束月份必须在1到12之间")
            if self.end_time_day < 1 or self.end_time_day > 31:
                raise ValidationError("结束日号必须在1到31之间")

            # 根据月份判断天数是否合法
            month = self.end_time_month
            day = self.end_time_day

            if month in [4, 6, 9, 11] and day > 30:
                raise ValidationError(f"结束日期的月份 {month} 的日期不能超过30天")
            elif month == 2 and day > 28:
                raise ValidationError("结束日期的2月日期不能超过28天")



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
