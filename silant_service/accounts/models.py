from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель пользователя"""
    ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('service', 'Сервисная организация'),
        ('manager', 'Менеджер'),
    )

    role = models.CharField('Роль', max_length=20, choices=ROLE_CHOICES, blank=True)
    phone = models.CharField('Телефон', max_length=20, blank=True)
    company_name = models.CharField('Название организации', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"