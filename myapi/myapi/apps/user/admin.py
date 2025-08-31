from django.contrib import admin

# 在此处注册您的模型。

admin.site.site_header = '宁夏特色作物气象灾害风险识别预测预警系统后端'  # 设置header
admin.site.site_title = '后端'  # 设置title
admin.site.index_title = '项目'

from django.contrib import admin
from .models import User


class UserModelAdmin(admin.ModelAdmin):
    """
    UserModelAdmin类继承自admin.ModelAdmin，用于定制用户模型在管理员界面的显示和操作。
    该类设置了用户列表的显示字段、过滤条件、搜索字段、每页显示数量、排序方式以及可编辑字段，
    并组织了用户信息的基本显示格式。
    """

    # 设置用户列表显示的字段
    list_display = ["username", "email", "wechat", "mobile", "is_active", "is_staff", "is_superuser", "city", "county",
                    "avatar", "get_province"]

    # 设置用户列表的过滤条件
    list_filter = ["is_active", "is_staff", "is_superuser", "city", "county"]

    # 设置用户列表的搜索字段
    search_fields = ["username", "email", "mobile", "city", "county"]

    # 设置每页显示的用户数量
    list_per_page = 10

    # 设置用户列表的排序方式，按ID降序排列
    ordering = ["-id"]

    # 设置用户列表中可直接编辑的字段
    list_editable = ["is_active", "is_staff", "is_superuser", "wechat", ]

    # 设置用户信息的字段集，将用户信息分为基本信息部分
    fieldsets = (
        ("基本信息", {
            "fields": ("username", "email", "mobile", "wechat", "city", "county"),
        }),
        ("权限信息", {
            "fields": ("is_active", "is_staff", "is_superuser"),
        }),
    )

    # 自定义方法：获取用户所在城市所属省份
    def get_province(self, obj):
        if obj.city and obj.city.province:
            return obj.city.province.name
        return "-"

    # 设置列标题
    get_province.short_description = "省份"
    # 允许按省份排序
    get_province.admin_order_field = "city__province__name"


admin.site.register(User, UserModelAdmin)

from .models import County


class CountyModelAdmin(admin.ModelAdmin):
    list_display = ["name", "city_belong"]
    list_filter = ["is_show", "city_belong"]  # 添加过滤器。
    search_fields = ["city_belong__name"]
    list_per_page = 10
    ordering = ["-id"]


admin.site.register(County, CountyModelAdmin)

from .models import City


class CityModelAdmin(admin.ModelAdmin):
    list_display = ["name"]  # 指定显示字段。
    # list_editable = ["is_show"]  # 设置可编辑字段。
    list_filter = ["is_show"]  # 添加过滤器。
    search_fields = ["name"]  # 支持按字段搜索。
    list_per_page = 10  # 每页显示记录数。
    ordering = ["-id"]  # 默认排序规则。
    actions_on_top = True  # 操作按钮位置。
    actions_on_bottom = True  # 操作按钮位置。
    save_on_top = True  # 顶部保存按钮。


admin.site.register(City, CityModelAdmin)

from .models import Province


class ProvinceModelAdmin(admin.ModelAdmin):
    list_display = ["name"]  # 添加字段。
    list_filter = ["is_show"]  # 添加过滤器。
    search_fields = ["name"]  # 支持按字段搜索。
    list_per_page = 10  # 每页显示记录数。
    ordering = ["-id"]  # 默认排序规则。
    actions_on_top = True  # 操作按钮位置。
    actions_on_bottom = True  # 操作按钮位置。
    save_on_top = True  # 顶部保存按钮。


admin.site.register(Province, ProvinceModelAdmin)
