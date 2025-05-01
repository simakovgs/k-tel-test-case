from django.urls import path

from django.urls import include, path
from rest_framework import routers

from .views import EquipmentViewSet, EquipmentTypeViewSet, EquipmentBulkCreateAPIView

router = routers.DefaultRouter()
router.register(r'equipment', EquipmentViewSet)
router.register(r'equipment_type', EquipmentTypeViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('api/equipment/bulk_create/', EquipmentBulkCreateAPIView.as_view(), name='equipment-bulk-create'),
]