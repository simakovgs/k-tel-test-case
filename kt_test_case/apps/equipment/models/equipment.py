from django.db import models

from kt_test_case.apps.core.models import BaseAbstractModel
from kt_test_case.apps.equipment.models.equipment_type import EquipmentType



class Equipment(BaseAbstractModel):
    """Оборудование"""

    type = models.ForeignKey(
        EquipmentType,
        on_delete=models.CASCADE,
        verbose_name="the related equipment type",
)
    serial_number = models.CharField(max_length=50, unique=True)
    note = models.TextField()

    def __str__(self):
        return self.serial_number

    class Meta:
        abstract = False
        ordering = ['updated_at']
