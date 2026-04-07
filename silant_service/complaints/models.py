from django.db import models
from django.conf import settings
from reference_books.models import FailureNode, RepairMethod, ServiceCompany  # исправлено
from machines.models import Machine
from datetime import date


class Complaint(models.Model):
    """Модель рекламации"""
    failure_date = models.DateField('Дата отказа')
    operating_hours = models.PositiveIntegerField('Наработка, м/час')
    failure_node = models.ForeignKey(FailureNode, on_delete=models.CASCADE, verbose_name='Узел отказа')
    failure_description = models.TextField('Описание отказа')
    repair_method = models.ForeignKey(RepairMethod, on_delete=models.CASCADE, verbose_name='Способ восстановления')
    used_parts = models.TextField('Используемые запасные части', blank=True)
    recovery_date = models.DateField('Дата восстановления')

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='complaints', verbose_name='Машина')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name='Сервисная компания')

    class Meta:
        verbose_name = 'Рекламация'
        verbose_name_plural = 'Рекламации'
        ordering = ['-failure_date']

    def __str__(self):
        return f"{self.machine.factory_number} - {self.failure_node.name} - {self.failure_date}"

    @property
    def downtime(self):
        """Расчет времени простоя (дни)"""
        if self.recovery_date and self.failure_date:
            return (self.recovery_date - self.failure_date).days
        return None