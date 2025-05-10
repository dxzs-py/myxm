from django.urls import path, re_path
from . import views
urlpatterns = [
    path(r'', views.MeteorologyViewSet.as_view({'get': 'list'}) ),
]