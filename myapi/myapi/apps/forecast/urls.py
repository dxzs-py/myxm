from django.urls import path
from .views import PredictionListView, TriggerPredictionView,DisasterIdentificationView

urlpatterns = [
    path('predictions/', PredictionListView.as_view(), name='prediction-list'),
    path('trigger-prediction/', TriggerPredictionView.as_view(), name='trigger-prediction'),
    path('disaster-identification/', DisasterIdentificationView.as_view(), name='disaster-identification'),
]