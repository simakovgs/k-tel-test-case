from rest_framework import permissions, viewsets, generics
from rest_framework.response import Response
from rest_framework import status

from ..models import Equipment
from ..serializers import (
    EquipmentSerializerReadOnly,
    EquipmentSerializerCreate,
    EquipmentSerializerPatchUpdate,
    EquipmentSerializerUpdate
)


class EquipmentViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = Equipment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return EquipmentSerializerReadOnly
        elif self.action == 'update':
            return EquipmentSerializerUpdate
        elif self.action == 'partial_update':
            return EquipmentSerializerPatchUpdate
        else:
            return EquipmentSerializerCreate

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create' and isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        if self.action == 'partial_update':
            kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)