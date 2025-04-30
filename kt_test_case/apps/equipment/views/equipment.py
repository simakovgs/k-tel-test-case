from rest_framework import generics
from ..models import Equipment
from ..serializers import EquipmentSerializer

# Список всего оборудования + создание
class EquipmentListCreateAPI(generics.ListCreateAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

# Просмотр/удаление конкретного оборудования
class EquipmentDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer