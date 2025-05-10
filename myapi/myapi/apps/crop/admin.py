from django.contrib import admin
import pandas as pd
from django.utils import timezone
# Register your models here.
from .models import City
class CityModelAdmin(admin.ModelAdmin):
    list_display = ["name"]  # 指定显示字段。
    # list_editable = ["is_show"]  # 设置可编辑字段。
    list_filter = ["is_show"]  # 添加过滤器。
    search_fields = ["name"]  # 支持按字段搜索。
    list_per_page = 10  # 每页显示记录数。
    ordering = ["-id"] # 默认排序规则。
    actions_on_top = True  # 操作按钮位置。
    actions_on_bottom = True  # 操作按钮位置。
    save_on_top = True  # 顶部保存按钮。
admin.site.register(City, CityModelAdmin)

from .models import Crop


class CropModelAdmin(admin.ModelAdmin):
    list_display = ["city", "begin_time", "end_time", "crop_class", "growth_cycle"]
    list_editable = ["begin_time", "end_time"]
    list_filter = ["city", "begin_time", "end_time"]
    search_fields = ["city__name", "crop_class"]
    list_per_page = 10
    ordering = ["-id"]
    actions_on_bottom = True
    save_on_top = True


admin.site.register(Crop, CropModelAdmin)
