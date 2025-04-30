from rest_framework import permissions, viewsets

from ..models import Equipment
from ..serializers import EquipmentSerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that ...
    """
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]
