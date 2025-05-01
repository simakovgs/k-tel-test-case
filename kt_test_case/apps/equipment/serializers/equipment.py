import re

from rest_framework import serializers
from rest_framework.validators import ValidationError

from ..models import Equipment, EquipmentType



class EquipmentSerializerReadOnly(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Equipment
        fields = [
            'id',
            'type',
            'serial_number',
            'created_at',
            'updated_at'
        ]


class EquipmentBulkCreateSerializer(serializers.ListSerializer):
    def create(self, validated_data):

        return Equipment.objects.bulk_create(
            [Equipment(**item) for item in validated_data]
        )

class EquipmentSerializerCreateUpdate(serializers.HyperlinkedModelSerializer):

    type_id = serializers.UUIDField(write_only=True)
    type = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='equipmenttype-detail'
    )


    def validate(self, data):
        """
        """
        validated_data = super().validate(data)

        current_serial_number = validated_data['serial_number']
        current_type: EquipmentType = EquipmentType.objects.get(id=validated_data['type_id'])
        print(current_type)
        current_serial_number_mask = current_type.serial_number_mask

        if len(current_serial_number) != len(current_serial_number_mask):
            raise serializers.ValidationError({
                'serial_number': f'Длина серийного номера должна быть {len(current_serial_number_mask)} символов'
            })

        regex_pattern = []
        for i, char in enumerate(current_serial_number_mask):
            if char == 'N':
                regex_pattern.append('[0-9]')
            elif char == 'A':
                regex_pattern.append('[A-Z]')
            elif char == 'a':
                regex_pattern.append('[a-z]')
            elif char == 'X':
                regex_pattern.append('[A-Z0-9]')
            elif char == 'Z':
                regex_pattern.append('[-_@]')
            else:
                raise serializers.ValidationError({
                    'serial_number_mask': f'Недопустимый {i} символ в маске {current_serial_number_mask}: {char}'
                })

        full_pattern = '^' + ''.join(regex_pattern) + '$'

        if not re.match(full_pattern, current_serial_number):
            raise serializers.ValidationError({
                'serial_number': 'Серийный номер не соответствует заданной маске'
            })

        return data

    class Meta:
        model = Equipment
        fields = [
            'id',
            'type',
            'type_id',
            'serial_number',
            'created_at',
            'updated_at'
        ]
        list_serializer_class = EquipmentBulkCreateSerializer
