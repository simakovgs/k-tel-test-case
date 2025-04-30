from django.urls import path

from django.urls import include, path
from rest_framework import routers

from .views import EquipmentViewSet, EquipmentTypeViewSet

router = routers.DefaultRouter()
router.register(r'equipment', EquipmentViewSet)
router.register(r'equipment_type', EquipmentTypeViewSet)



urlpatterns = [
    path('', include(router.urls)),
]