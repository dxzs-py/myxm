from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest
from rest_framework.parsers import JSONParser
from django.db import models


# 创建一个简单的视图类来处理forecast相关操作
class ForecastAdminSite(admin.ModelAdmin):
    """Forecast应用的自定义Admin界面

    该类提供了一个不依赖数据库模型的自定义管理界面，
    允许通过Django Admin界面触发预测任务和查看预测结果。
    """

    def get_urls(self):
        """添加自定义URL

        扩展默认的admin URLs，添加预测管理相关的自定义页面路由。

        Returns:
            list: 包含默认URL和自定义URL的列表
        """
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_site.admin_view(self.forecast_main_view), name='forecast-main'),
            path('trigger/', self.admin_site.admin_view(self.trigger_forecast), name='forecast-trigger'),
            path('results/', self.admin_site.admin_view(self.view_results), name='forecast-results'),
        ]
        return custom_urls + urls

    def forecast_main_view(self, request):
        """主页面视图

        显示预测管理的主页面，提供触发预测任务和查看预测结果的入口。

        Args:
            request (HttpRequest): HTTP请求对象

        Returns:
            HttpResponse: 渲染后的主页面模板响应
        """
        context = dict(
            self.admin_site.each_context(request),
            title="预测管理",
        )
        return render(request, 'admin/forecast_main.html', context)

    def trigger_forecast(self, request):
        """触发预测任务

        通过调用TriggerPredictionView视图类来手动触发预测任务。

        Args:
            request (HttpRequest): HTTP请求对象，应为POST方法

        Returns:
            HttpResponse: 重定向到预测管理主页面的响应
        """
        if request.method == 'POST':
            try:
                # 直接调用已有的视图类
                from myapi.apps.forecast.views import TriggerPredictionView

                # 创建一个模拟请求
                api_request = HttpRequest()
                api_request.method = 'POST'
                api_request.user = request.user
                api_request._full_data = {'target_indices': [0, 1, 2, 3, 4, 5, 6]}
                api_request.META = request.META
                api_request.parsers = [JSONParser()]
                api_request.data = {'target_indices': [0, 1, 2, 3, 4, 5, 6]}

                # 实例化视图并处理请求
                view = TriggerPredictionView()
                response = view.post(api_request)

                if response.status_code == 202:
                    messages.success(request, '预测任务已成功提交')
                else:
                    messages.error(request, f'预测任务提交失败: {response.data.get("error", "未知错误")}')
            except Exception as e:
                messages.error(request, f'预测任务提交异常: {str(e)}')

        return redirect(reverse('admin:forecast_forecast_changelist'))

    def view_results(self, request):
        """查看预测结果

        通过调用PredictionListView视图类获取并展示最新的预测结果。

        Args:
            request (HttpRequest): HTTP请求对象

        Returns:
            HttpResponse: 渲染后的预测结果页面模板响应
        """
        try:
            # 调用已有的视图类获取预测结果
            from myapi.apps.forecast.views import PredictionListView

            api_request = HttpRequest()
            api_request.method = 'GET'
            api_request.user = request.user
            api_request.META = request.META
            api_request.query_params = {}

            view = PredictionListView()
            response = view.get(api_request)

            context = dict(
                self.admin_site.each_context(request),  # Admin 模板提供上下文变量
                title="预测结果",
                results=response.data if response.status_code == 200 else None,
            )
            return render(request, 'admin/forecast_results.html', context)
        except Exception as e:
            messages.error(request, f'获取预测结果异常: {str(e)}')
            return redirect(reverse('admin:forecast_forecast_changelist'))

    def has_add_permission(self, request):
        """控制添加权限

        禁用添加新对象的权限，因为这是一个虚拟模型。

        Args:
            request (HttpRequest): HTTP请求对象

        Returns:
            bool: 始终返回False，禁用添加权限
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """控制删除权限

        禁用删除对象的权限，因为这是一个虚拟模型。

        Args:
            request (HttpRequest): HTTP请求对象
            obj: 要删除的对象实例

        Returns:
            bool: 始终返回False，禁用删除权限
        """
        return False

    def has_change_permission(self, request, obj=None):
        """控制修改权限

        禁用修改对象的权限，因为这是一个虚拟模型。

        Args:
            request (HttpRequest): HTTP请求对象
            obj: 要修改的对象实例

        Returns:
            bool: 始终返回False，禁用修改权限
        """
        return False

    def has_module_permission(self, request):
        """控制模块访问权限

        控制用户是否有权访问该模块。

        Args:
            request (HttpRequest): HTTP请求对象

        Returns:
            bool: 如果用户是工作人员则返回True，否则返回False
        """
        return request.user.is_staff


# 创建一个虚拟模型用于注册admin
class Forecast(models.Model):
    """虚拟模型类

    用于在Django Admin中注册ForecastAdminSite的虚拟模型，
    不会创建实际的数据库表。
    """

    class Meta:
        managed = False  # 不创建数据库表
        verbose_name = "预测管理"
        verbose_name_plural = "预测管理"


# 注册到admin站点
admin.site.register(Forecast, ForecastAdminSite)
