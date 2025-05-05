from django.core.exceptions import ObjectDoesNotExist
from ..models import Equipment

class EquipmentService:
    @staticmethod
    def get_by_serial_number(serial_number):
        try:
            return Equipment.objects.get(serial_number=serial_number)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_by_note(note):
        return Equipment.objects.filter(note=note)