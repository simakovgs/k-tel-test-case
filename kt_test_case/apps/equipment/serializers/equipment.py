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
            'note',
            'created_at',
            'updated_at'
        ]


class EquipmentSerializerCreateUpdate(serializers.HyperlinkedModelSerializer):

    type: EquipmentType = serializers.HyperlinkedRelatedField(
        required=True,
        queryset=EquipmentType.objects.all(),
        view_name='equipmenttype-detail',
    )
    note = serializers.CharField(required=False)

    def validate(self, data):
        """
        """
        validated_data = super().validate(data)

        current_serial_number = validated_data['serial_number']
        current_type: EquipmentType = validated_data['type']
        current_serial_number_mask = current_type.serial_number_mask

        # Проверяем соответствие длины
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
            'serial_number',
            'note',
            'created_at',
            'updated_at'
        ]