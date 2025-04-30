from rest_framework import permissions, viewsets

from ..models import EquipmentType
from ..serializers import EquipmentTypeSerializer

class EquipmentTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that ...
    """
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
