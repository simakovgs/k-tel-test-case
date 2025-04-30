from rest_framework import serializers
from ..models import EquipmentType

class EquipmentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EquipmentType
        fields = [
            'id',
            'name',
            'serial_number_mask',
            'created_at',
            'updated_at'
        ]