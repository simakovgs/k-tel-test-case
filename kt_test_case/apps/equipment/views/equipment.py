from rest_framework import permissions, viewsets, generics
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

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create' and isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)