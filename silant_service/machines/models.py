from django.db import models
from django.conf import settings
from reference_books.models import (
    TechniqueModel, EngineModel, TransmissionModel,
    DriveAxleModel, SteerAxleModel, ServiceCompany
)


class Machine(models.Model):
    """Модель машины"""
    factory_number = models.CharField('Зав. № машины', max_length=50, unique=True)
    technique_model = models.ForeignKey(TechniqueModel, on_delete=models.CASCADE, verbose_name='Модель техники')
    engine_model = models.ForeignKey(EngineModel, on_delete=models.CASCADE, verbose_name='Модель двигателя')
    engine_number = models.CharField('Зав. № двигателя', max_length=50)
    transmission_model = models.ForeignKey(TransmissionModel, on_delete=models.CASCADE,
                                           verbose_name='Модель трансмиссии')
    transmission_number = models.CharField('Зав. № трансмиссии', max_length=50)
    drive_axle_model = models.ForeignKey(DriveAxleModel, on_delete=models.CASCADE, verbose_name='Модель ведущего моста')
    drive_axle_number = models.CharField('Зав. № ведущего моста', max_length=50)
    steer_axle_model = models.ForeignKey(SteerAxleModel, on_delete=models.CASCADE,
                                         verbose_name='Модель управляемого моста')
    steer_axle_number = models.CharField('Зав. № управляемого моста', max_length=50)

    supply_contract = models.CharField('Договор поставки №, дата', max_length=100)
    shipping_date = models.DateField('Дата отгрузки с завода')
    consignee = models.CharField('Грузополучатель (конечный потребитель)', max_length=200)
    delivery_address = models.TextField('Адрес поставки (эксплуатации)')
    equipment = models.TextField('Комплектация (доп. опции)', blank=True)

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='machines_as_client',
        verbose_name='Клиент',
        limit_choices_to={'role': 'client'}
    )
    service_company = models.ForeignKey(
        ServiceCompany,
        on_delete=models.CASCADE,
        verbose_name='Сервисная компания'
    )

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'
        ordering = ['-shipping_date']

    def __str__(self):
        return f"{self.technique_model.name} - {self.factory_number}"