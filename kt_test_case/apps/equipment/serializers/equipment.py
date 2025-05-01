import re

from rest_framework import serializers
from rest_framework.validators import ValidationError

from ..models import Equipment, EquipmentType
from ..utils import validate_sn


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

    def validate(self, data):
        """
        """


        ######################
        #     POST VALIDATION HERE!!
        ######################

        validated_data = super().validate(data)



        current_serial_number = validated_data['serial_number']
        current_type: EquipmentType = EquipmentType.objects.get(id=validated_data['type_id'])
        current_serial_number_mask = current_type.serial_number_mask

        validate_sn(sn=current_serial_number, snm=current_serial_number_mask)

        return data

    # def create(self, validated_data):
    #
    #     return Equipment.objects.bulk_create(
    #         [Equipment(**item) for item in validated_data]
    #     )

class EquipmentSerializerCreateUpdate(serializers.HyperlinkedModelSerializer):

    type_id = serializers.UUIDField(write_only=True)
    type = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='equipmenttype-detail'
    )


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
