from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from machines.models import Machine
from maintenances.models import Maintenance
from complaints.models import Complaint
from .serializers import (
    MachineSerializer, MaintenanceSerializer, ComplaintSerializer
)


class IsManagerOrReadOnly(permissions.BasePermission):
    """Только менеджер может изменять данные"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_superuser or 
            request.user.groups.filter(name='Менеджер').exists()
        )


class MachineListAPIView(generics.ListAPIView):
    """API для получения списка машин"""
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        
        # Для неавторизованных - только базовые поля (1-10)
        if not user.is_authenticated:
            return Machine.objects.all()
        
        # Для авторизованных - с учётом прав
        if user.is_superuser or user.groups.filter(name='Менеджер').exists():
            return Machine.objects.all()
        elif user.groups.filter(name='Клиент').exists():
            return Machine.objects.filter(client=user)
        elif user.groups.filter(name='Сервисная организация').exists():
            return Machine.objects.filter(service_company__name=user.company_name)
        return Machine.objects.none()


class MachineDetailAPIView(generics.RetrieveAPIView):
    """API для получения детальной информации о машине"""
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MaintenanceListAPIView(generics.ListAPIView):
    """API для получения списка ТО"""
    serializer_class = MaintenanceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        
        if not user.is_authenticated:
            return Maintenance.objects.none()
        
        if user.is_superuser or user.groups.filter(name='Менеджер').exists():
            return Maintenance.objects.all()
        elif user.groups.filter(name='Клиент').exists():
            return Maintenance.objects.filter(machine__client=user)
        elif user.groups.filter(name='Сервисная организация').exists():
            return Maintenance.objects.filter(machine__service_company__name=user.company_name)
        return Maintenance.objects.none()


class MaintenanceDetailAPIView(generics.RetrieveAPIView):
    """API для получения детальной информации о ТО"""
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ComplaintListAPIView(generics.ListAPIView):
    """API для получения списка рекламаций"""
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        
        if not user.is_authenticated:
            return Complaint.objects.none()
        
        if user.is_superuser or user.groups.filter(name='Менеджер').exists():
            return Complaint.objects.all()
        elif user.groups.filter(name='Клиент').exists():
            return Complaint.objects.filter(machine__client=user)
        elif user.groups.filter(name='Сервисная организация').exists():
            return Complaint.objects.filter(machine__service_company__name=user.company_name)
        return Complaint.objects.none()


class ComplaintDetailAPIView(generics.RetrieveAPIView):
    """API для получения детальной информации о рекламации"""
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class APIRootView(APIView):
    """Корень API со ссылками на все endpoints"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            'machines': {
                'url': '/api/machines/',
                'description': 'Список всех машин'
            },
            'machine_detail': {
                'url': '/api/machines/{id}/',
                'description': 'Детальная информация о машине'
            },
            'maintenances': {
                'url': '/api/maintenances/',
                'description': 'Список всех ТО'
            },
            'maintenance_detail': {
                'url': '/api/maintenances/{id}/',
                'description': 'Детальная информация о ТО'
            },
            'complaints': {
                'url': '/api/complaints/',
                'description': 'Список всех рекламаций'
            },
            'complaint_detail': {
                'url': '/api/complaints/{id}/',
                'description': 'Детальная информация о рекламации'
            }
        })