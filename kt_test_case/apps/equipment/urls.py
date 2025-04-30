from django.urls import path
from .views import EquipmentListCreateAPI, EquipmentDetailAPI

urlpatterns = [
    path('api/equipment/', EquipmentListCreateAPI.as_view(), name='equipment-list'),
    path('api/equipment/<int:pk>/', EquipmentDetailAPI.as_view(), name='equipment-detail'),
]