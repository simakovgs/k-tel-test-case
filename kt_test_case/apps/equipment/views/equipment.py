from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status

from ..models import Equipment
from ..serializers import EquipmentSerializerReadOnly, EquipmentSerializerCreateUpdate

class EquipmentViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = Equipment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return EquipmentSerializerReadOnly
        return EquipmentSerializerCreateUpdate
