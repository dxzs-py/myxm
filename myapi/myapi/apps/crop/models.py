from django.db import models

# Create your models here.
from myapi.utils.models import BaseModel

class City(BaseModel):
    name = models.CharField(max_length=64, verbose_name="城市名称")

    class  Meta:
        db_table = "xm_city"
        verbose_name = "城市"
        verbose_name_plural = "城市"
    def __str__(self):
        return "%s" %self.name

class Crop(BaseModel):
    begin_time = models.DateField (verbose_name="开始日期")
    end_time = models.DateField(verbose_name="结束日期")
    city = models.ForeignKey(
        "City",
        on_delete=models.PROTECT,
        verbose_name="城市",
        default= "get_default_city_id"
    )
    crop_class = models.CharField(max_length=64, verbose_name="作物名称")
    growth_cycle = models.CharField(max_length=64, verbose_name="成长周期")



    class Meta:
        db_table = "xm_crop"
        verbose_name = "作物"
        verbose_name_plural = "作物"
    def __str__(self):
        return f"{self.begin_time} - {self.city.name} - {self.end_time}"

    @staticmethod
    def get_default_city_id():
        city, _ = City.objects.get_or_create(name="银川")
        return city.id



