from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from machines.models import Machine
from maintenances.models import Maintenance
from complaints.models import Complaint
from reference_books.models import (
    TechniqueModel, EngineModel, TransmissionModel,
    DriveAxleModel, SteerAxleModel, MaintenanceType,
    FailureNode, RepairMethod, ServiceCompany
)


class Command(BaseCommand):
    help = 'Создание групп и прав доступа'

    def handle(self, *args, **options):
        # Создаем группы
        client_group, _ = Group.objects.get_or_create(name='Клиент')
        service_group, _ = Group.objects.get_or_create(name='Сервисная организация')
        manager_group, _ = Group.objects.get_or_create(name='Менеджер')

        # Получаем все ContentType для моделей
        machine_ct = ContentType.objects.get_for_model(Machine)
        maintenance_ct = ContentType.objects.get_for_model(Maintenance)
        complaint_ct = ContentType.objects.get_for_model(Complaint)

        # Справочники
        technique_ct = ContentType.objects.get_for_model(TechniqueModel)
        engine_ct = ContentType.objects.get_for_model(EngineModel)
        transmission_ct = ContentType.objects.get_for_model(TransmissionModel)
        drive_axle_ct = ContentType.objects.get_for_model(DriveAxleModel)
        steer_axle_ct = ContentType.objects.get_for_model(SteerAxleModel)
        maintenance_type_ct = ContentType.objects.get_for_model(MaintenanceType)
        failure_node_ct = ContentType.objects.get_for_model(FailureNode)
        repair_method_ct = ContentType.objects.get_for_model(RepairMethod)
        service_company_ct = ContentType.objects.get_for_model(ServiceCompany)

        # ========== КЛИЕНТ ==========
        # Машина: только просмотр
        client_perms = [
            Permission.objects.get(codename='view_machine', content_type=machine_ct),
            # ТО: просмотр и добавление
            Permission.objects.get(codename='view_maintenance', content_type=maintenance_ct),
            Permission.objects.get(codename='add_maintenance', content_type=maintenance_ct),
            # Рекламации: только просмотр
            Permission.objects.get(codename='view_complaint', content_type=complaint_ct),
        ]
        client_group.permissions.set(client_perms)

        # ========== СЕРВИСНАЯ ОРГАНИЗАЦИЯ ==========
        service_perms = [
            # Машина: просмотр
            Permission.objects.get(codename='view_machine', content_type=machine_ct),
            # ТО: просмотр, добавление, изменение
            Permission.objects.get(codename='view_maintenance', content_type=maintenance_ct),
            Permission.objects.get(codename='add_maintenance', content_type=maintenance_ct),
            Permission.objects.get(codename='change_maintenance', content_type=maintenance_ct),
            # Рекламации: просмотр, добавление, изменение
            Permission.objects.get(codename='view_complaint', content_type=complaint_ct),
            Permission.objects.get(codename='add_complaint', content_type=complaint_ct),
            Permission.objects.get(codename='change_complaint', content_type=complaint_ct),
        ]
        service_group.permissions.set(service_perms)

        # ========== МЕНЕДЖЕР ==========
        # Полный доступ ко всему
        all_perms = Permission.objects.all()
        manager_group.permissions.set(all_perms)

        self.stdout.write(self.style.SUCCESS('Группы и права успешно созданы'))