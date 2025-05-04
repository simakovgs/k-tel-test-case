from rest_framework import permissions, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from ..models import Equipment
from ..serializers import (
    EquipmentSerializerReadOnly,
    EquipmentSerializerCreate,
    EquipmentSerializerPatchUpdate,
    EquipmentSerializerUpdate
)
from ..services import EquipmentService


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'  # Это значение по умолчанию, можно явно указать

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'by_serial_number', 'by_note']:
            return EquipmentSerializerReadOnly
        elif self.action == 'update':
            return EquipmentSerializerUpdate
        elif self.action == 'partial_update':
            return EquipmentSerializerPatchUpdate
        else:
            return EquipmentSerializerCreate

    @action(detail=False, url_path='serial-number/(?P<serial_number>[^/.]+)')
    def by_serial_number(self, request, serial_number):
        equipment = EquipmentService.get_by_serial_number(serial_number)
        if not equipment:
            return Response(status=404)
        return Response(self.get_serializer(equipment).data)

    @action(detail=False, url_path='note/(?P<note>[^/.]+)')
    def by_note(self, request, note):
        equipments = EquipmentService.get_by_note(note)
        return Response(self.get_serializer(equipments, many=True).data)


    def get_serializer(self, *args, **kwargs):
        if self.action == 'create' and isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        if self.action == 'partial_update':
            kwargs['partial'] = True
        return super().get_serializer(*args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT, headers=headers)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=False)
        self.perform_create(serializer)

        response_data = {
            'created_count': len(serializer.validated_data) if hasattr(serializer, 'validated_data') else 0,
            'created_objects': serializer.data,
            'errors': getattr(serializer, 'validation_errors', []),
        }
        headers = self.get_success_headers(serializer.data)
        status_code = status.HTTP_207_MULTI_STATUS if response_data['errors'] else status.HTTP_201_CREATED
        return Response(response_data, status=status_code, headers=headers)