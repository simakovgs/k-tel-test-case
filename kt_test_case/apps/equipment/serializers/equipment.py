from rest_framework import serializers

from kt_test_case.apps.equipment.models import Equipment, EquipmentType
from kt_test_case.apps.equipment.utils import validate_sn


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

class EquipmentSerializerUpdate(serializers.HyperlinkedModelSerializer):
    type_id = serializers.UUIDField(write_only=True)
    type = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='equipmenttype-detail'
    )
    def validate(self, data):
        validated_data = super().validate(data)
        current_serial_number = validated_data['serial_number']
        current_type = EquipmentType.objects.filter(id=validated_data['type_id']).first()
        if not current_type:
            raise serializers.ValidationError({
                'type_id': f"Тип оборудования {validated_data['type_id']} не найден"
            })
        current_serial_number_mask = current_type.serial_number_mask
        validate_sn(sn=current_serial_number, snm=current_serial_number_mask)
        return data

    class Meta:
        model = Equipment
        fields = [
            'id',
            'type',
            'type_id',
            'note',
            'serial_number',
            'created_at',
            'updated_at'
        ]


class EquipmentSerializerPatchUpdate(serializers.HyperlinkedModelSerializer):
    type_id = serializers.UUIDField(write_only=True)
    type = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='equipmenttype-detail'
    )
    def validate(self, data):
        validated_data = super().validate(data)

        if 'serial_number' in validated_data and 'type_id' in validated_data:
            current_serial_number = validated_data['serial_number']
            current_type = EquipmentType.objects.filter(id=validated_data['type_id']).first()
            if not current_type:
                raise serializers.ValidationError({
                    'type_id': f"Тип оборудования {validated_data['type_id']} не найден"
                })
            current_serial_number_mask = current_type.serial_number_mask
            validate_sn(sn=current_serial_number, snm=current_serial_number_mask)

        if 'serial_number' in validated_data and not 'type_id' in validated_data:
            current_serial_number = validated_data['serial_number']
            current_type = EquipmentType.objects.filter(id=self.instance.type_id).first()
            current_serial_number_mask = current_type.serial_number_mask
            validate_sn(sn=current_serial_number, snm=current_serial_number_mask)

        if not 'serial_number' in validated_data and 'type_id' in validated_data:
            raise serializers.ValidationError({
                'type_id': f"Смена типа оборудования осуществляется с указанием нового серийного номера"
            })

        return data

    class Meta:
        model = Equipment
        fields = [
            'id',
            'type',
            'type_id',
            'note',
            'serial_number',
            'created_at',
            'updated_at'
        ]


class EquipmentBulkCreateSerializer(serializers.ListSerializer):

    def validate(self, data):
        valid_data = []
        self.validation_errors = []

        for idx, item in enumerate(data):
            item_errors = {}
            existed_sn = Equipment.objects.filter(serial_number=item['serial_number']).first()
            current_type = EquipmentType.objects.filter(id=item['type_id']).first()

            if existed_sn:
                item_errors['serial_number'] = (f"Оборудование с серийным номером "
                                                f"{item['serial_number']} "
                                                f"уже существует")

            if current_type:
                current_snm = current_type.serial_number_mask
                try:
                    validate_sn(sn=item['serial_number'], snm=current_snm)
                except serializers.ValidationError as e:
                    item_errors['serial_number'] = [str(err) for err in e.detail]
            else:
                item_errors['type_id'] = f"Тип оборудования {item['type_id']} не найден"

            if not item_errors:
                valid_data.append(item)
            else:
                self.validation_errors.append({
                    'index': idx,
                    'data': item,
                    'errors': item_errors,
                })

        return valid_data

class EquipmentSerializerCreate(serializers.HyperlinkedModelSerializer):
    type_id = serializers.UUIDField(write_only=True, required=True)
    type = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='equipmenttype-detail'
    )
    serial_number =  serializers.CharField(required=True)
    note = serializers.CharField(max_length=150, required=False)


    class Meta:
        model = Equipment
        fields = [
            'id',
            'type',
            'type_id',
            'note',
            'serial_number',
            'created_at',
            'updated_at'
        ]
        list_serializer_class = EquipmentBulkCreateSerializer
