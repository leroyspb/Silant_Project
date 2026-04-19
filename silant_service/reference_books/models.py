from django.db import models


class BaseReference(models.Model):
    """Базовая модель для справочников"""
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class TechniqueModel(BaseReference):
    """Модель техники"""

    class Meta:
        verbose_name = 'Модель техники'
        verbose_name_plural = 'Модели техники'


class EngineModel(BaseReference):
    """Модель двигателя"""

    class Meta:
        verbose_name = 'Модель двигателя'
        verbose_name_plural = 'Модели двигателей'


class TransmissionModel(BaseReference):
    """Модель трансмиссии"""

    class Meta:
        verbose_name = 'Модель трансмиссии'
        verbose_name_plural = 'Модели трансмиссий'


class DriveAxleModel(BaseReference):
    """Модель ведущего моста"""

    class Meta:
        verbose_name = 'Модель ведущего моста'
        verbose_name_plural = 'Модели ведущих мостов'


class SteerAxleModel(BaseReference):
    """Модель управляемого моста"""

    class Meta:
        verbose_name = 'Модель управляемого моста'
        verbose_name_plural = 'Модели управляемых мостов'


class MaintenanceType(BaseReference):
    """Вид ТО"""

    class Meta:
        verbose_name = 'Вид ТО'
        verbose_name_plural = 'Виды ТО'


class FailureNode(BaseReference):
    """Узел отказа"""

    class Meta:
        verbose_name = 'Узел отказа'
        verbose_name_plural = 'Узлы отказа'


class RepairMethod(BaseReference):
    """Способ восстановления"""

    class Meta:
        verbose_name = 'Способ восстановления'
        verbose_name_plural = 'Способы восстановления'


class ServiceCompany(BaseReference):
    """Сервисная компания"""

    class Meta:
        verbose_name = 'Сервисная компания'
        verbose_name_plural = 'Сервисные компании'

