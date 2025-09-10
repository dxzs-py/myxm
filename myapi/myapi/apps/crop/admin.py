from django.contrib import admin

# Register your models here.

from .models import Growth


class GrowthModelAdmin(admin.ModelAdmin):
    list_display = ('growth_cycle', 'display_begin_time', 'display_end_time', 'crop', 'is_critical')
    list_filter = ('crop', 'is_critical')
    search_fields = ["growth_cycle", "crop__crop_class"]
    list_per_page = 10
    ordering = ["-id"]

    # 自定义显示开始日期
    def display_begin_time(self, obj):
        if obj.begin_time_month and obj.begin_time_day:
            return f"{obj.begin_time_month}月{obj.begin_time_day}日"
        return "N/A"

    display_begin_time.short_description = '开始日期'

    # 自定义显示结束日期
    def display_end_time(self, obj):
        if obj.end_time_month and obj.end_time_day:
            return f"{obj.end_time_month}月{obj.end_time_day}日"
        return "N/A"

    display_end_time.short_description = '结束日期'


admin.site.register(Growth, GrowthModelAdmin)

from .models import PlantArea


class PlantAreaModelAdmin(admin.ModelAdmin):
    list_display = ["name", "crop", "city", "area", "longitude", "latitude", "including_areas"]
    list_filter = ["is_show", "city", "crop"]  # 添加过滤器。
    search_fields = ["city__name", "crop__crop_class"]
    list_per_page = 10
    ordering = ["-id"]


admin.site.register(PlantArea, PlantAreaModelAdmin)

from .models import Crop


class CropModelAdmin(admin.ModelAdmin):
    list_display = ["crop_class"]
    list_filter = ["is_show", "crop_class"]  # 添加过滤器。
    search_fields = ["crop_class"]
    list_per_page = 10
    ordering = ["-id"]


admin.site.register(Crop, CropModelAdmin)
