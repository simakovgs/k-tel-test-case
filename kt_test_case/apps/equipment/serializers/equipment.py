from rest_framework import serializers
from ..models import Equipment

class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Equipment
        fields = [
            'id',
            'type',
            'serial_number',
            'note',
            'created_at',
            'updated_at'
        ]