from django.contrib import admin

# Register your models here.

from .models import Growth
class GrowthModelAdmin(admin.ModelAdmin):
    list_display = ["growth_cycle", "begin_time", "end_time", "growth_temp_min", "growth_temp_max",
                     "growth_humidity_min",
                     "growth_humidity_max", "growth_rainfall_min", "growth_rainfall_max", "growth_wind_min",
                     "sunshine_hours_max"]
    list_filter = ["is_show"]  # 添加过滤器。
    search_fields = ["growth_cycle","crop__crop_class"]
    list_per_page = 10
    ordering = ["-id"]


admin.site.register(Growth, GrowthModelAdmin)


from .models import PlantArea
class PlantAreaModelAdmin(admin.ModelAdmin):
    list_display = ["name","crop","city","area","longitude","latitude","including_areas"]
    list_filter = ["is_show","city","crop"]  # 添加过滤器。
    search_fields = ["city__name","crop__crop_class"]
    list_per_page = 10
    ordering = ["-id"]


admin.site.register(PlantArea, PlantAreaModelAdmin)

from .models import Crop
class CropModelAdmin(admin.ModelAdmin):
    list_display = ["crop_class"]
    list_filter = ["is_show","crop_class"]  # 添加过滤器。
    search_fields = ["crop_class"]
    list_per_page = 10
    ordering = ["-id"]


admin.site.register(Crop, CropModelAdmin)


