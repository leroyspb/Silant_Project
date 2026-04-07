from django.db import models
from django.conf import settings
from reference_books.models import MaintenanceType, ServiceCompany  # исправлено
from machines.models import Machine


class Maintenance(models.Model):
    """Модель технического обслуживания"""
    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.CASCADE, verbose_name='Вид ТО')
    maintenance_date = models.DateField('Дата проведения ТО')
    operating_hours = models.PositiveIntegerField('Наработка, м/час')
    work_order_number = models.CharField('№ заказ-наряда', max_length=50)
    work_order_date = models.DateField('Дата заказ-наряда')

    organization = models.ForeignKey(
        ServiceCompany,
        on_delete=models.CASCADE,
        verbose_name='Организация, проводившая ТО',
        related_name='maintenances_as_organization'
    )
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='maintenances', verbose_name='Машина')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, verbose_name='Сервисная компания')

    class Meta:
        verbose_name = 'Техническое обслуживание'
        verbose_name_plural = 'Технические обслуживания'
        ordering = ['-maintenance_date']

    def __str__(self):
        return f"{self.machine.factory_number} - {self.maintenance_type.name} - {self.maintenance_date}"