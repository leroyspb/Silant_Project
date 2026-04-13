from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


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


@receiver(post_save, sender=User)
def assign_user_group(sender, instance, created, **kwargs):
    """Автоматическое назначение группы при создании пользователя"""
    if created and instance.role:
        from django.contrib.auth.models import Group

        if instance.role == 'client':
            group = Group.objects.get(name='Клиент')
        elif instance.role == 'service':
            group = Group.objects.get(name='Сервисная организация')
        elif instance.role == 'manager':
            group = Group.objects.get(name='Менеджер')
        else:
            return

        instance.groups.add(group)