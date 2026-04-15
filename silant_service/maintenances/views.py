from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Maintenance
from reference_books.models import MaintenanceType, ServiceCompany


class MaintenanceListView(LoginRequiredMixin, ListView):
    model = Maintenance
    template_name = 'maintenances/maintenance_list.html'
    context_object_name = 'maintenances'
    
    def get_queryset(self):
        user = self.request.user
        machine_id = self.request.GET.get('machine')
        
        # Базовый queryset в зависимости от роли
        if user.is_superuser or user.groups.filter(name='Менеджер').exists():
            queryset = Maintenance.objects.all()
        elif user.groups.filter(name='Клиент').exists():
            queryset = Maintenance.objects.filter(machine__client=user)
        elif user.groups.filter(name='Сервисная организация').exists():
            queryset = Maintenance.objects.filter(service_company__name=user.company_name)
        else:
            queryset = Maintenance.objects.none()
        
        # Фильтрация
        maintenance_type = self.request.GET.get('maintenance_type')
        if maintenance_type:
            queryset = queryset.filter(maintenance_type_id=maintenance_type)
        
        if machine_id:
            queryset = queryset.filter(machine__factory_number__icontains=machine_id)
        
        service_company = self.request.GET.get('service_company')
        if service_company:
            queryset = queryset.filter(service_company_id=service_company)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Данные для фильтров
        context['maintenance_types'] = MaintenanceType.objects.all()
        context['service_companies'] = ServiceCompany.objects.all()
        
        # Выбранные значения
        context['selected_type'] = self.request.GET.get('maintenance_type', '')
        context['selected_machine'] = self.request.GET.get('machine', '')
        context['selected_service'] = self.request.GET.get('service_company', '')
        
        return context


class MaintenanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Maintenance
    fields = ['maintenance_type', 'maintenance_date', 'operating_hours', 
              'work_order_number', 'work_order_date', 'organization', 'service_company']
    template_name = 'maintenances/maintenance_form.html'
    
    def test_func(self):
        user = self.request.user
        maintenance = self.get_object()
        
        is_client = user.groups.filter(name='Клиент').exists()
        is_service = user.groups.filter(name='Сервисная организация').exists()
        is_manager = user.is_superuser or user.groups.filter(name='Менеджер').exists()
        
        if is_client:
            return maintenance.machine.client == user
        elif is_service:
            return maintenance.service_company.name == user.company_name
        elif is_manager:
            return True
        return False
    
    def get_success_url(self):
        return reverse_lazy('machine_detail', kwargs={'pk': self.object.machine.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.get_object().machine
        return context