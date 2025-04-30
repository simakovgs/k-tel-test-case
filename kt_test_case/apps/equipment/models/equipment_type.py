# name, mask

from django.db import models

from kt_test_case.apps.core.models import BaseAbstractModel

class EquipmentType(BaseAbstractModel):
    """Тип оборудования"""

    name = models.CharField(max_length=50)
    serial_number_mask = models.CharField(max_length=50)


    def __str__(self):
        return self.name

    class Meta:
        abstract = False
        ordering = ['updated_at']
