from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'growth/', views.GrowthListAPIView.as_view()),
    path(r"plantArea/", views.PlantAreaListAPIView.as_view()),
    path(r"cropClass/", views.CropListAPIView.as_view()),
]
