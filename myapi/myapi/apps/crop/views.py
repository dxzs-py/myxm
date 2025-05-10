from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Crop
from .serializers import CropSerializer
# Create your views here.
class CropListAPIView(ListAPIView):
    queryset = Crop.objects.filter(is_show=True).order_by("-id")
    serializer_class = CropSerializer

