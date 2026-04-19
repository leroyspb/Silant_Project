from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Maintenance
from .forms import MaintenanceForm
from reference_books.models import MaintenanceType, ServiceCompany
from machines.models import Machine

class MaintenanceListView(LoginRequiredMixin, ListView):
    model = Maintenance
    template_name = 'maintenances/maintenance_list.html'
    context_object_name = 'maintenances'
    
    def get_queryset(self):
        user = self.request.user
        
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
        
        machine_number = self.request.GET.get('machine_number')
        if machine_number:
            queryset = queryset.filter(machine__factory_number__icontains=machine_number)
        
        service_company = self.request.GET.get('service_company')
        if service_company:
            queryset = queryset.filter(service_company_id=service_company)
        
        return queryset.order_by('-maintenance_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['maintenance_types'] = MaintenanceType.objects.all()
        context['service_companies'] = ServiceCompany.objects.all()
        context['machines'] = Machine.objects.all()  # для фильтра по номеру
        
        context['selected_type'] = self.request.GET.get('maintenance_type', '')
        context['selected_machine_number'] = self.request.GET.get('machine_number', '')
        context['selected_service'] = self.request.GET.get('service_company', '')
        
        context['is_manager'] = user.is_superuser or user.groups.filter(name='Менеджер').exists()
        context['is_service'] = user.groups.filter(name='Сервисная организация').exists()
        
        return context


class MaintenanceCreateView(LoginRequiredMixin, CreateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenances/maintenance_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        machine = get_object_or_404(Machine, pk=self.kwargs['machine_pk'])
        
        # Проверяем права доступа
        if user.is_superuser or user.groups.filter(name='Менеджер').exists():
            pass  # Менеджер может всё
        elif user.groups.filter(name='Клиент').exists():
            # Клиент может добавлять ТО только для своих машин
            if machine.client != user:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden("У вас нет прав для добавления ТО к этой машине")
        elif user.groups.filter(name='Сервисная организация').exists():
            # Сервисная компания может добавлять ТО для своих машин
            if machine.service_company.name != user.company_name:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden("У вас нет прав для добавления ТО к этой машине")
        else:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("У вас нет прав для добавления ТО")
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        machine = get_object_or_404(Machine, pk=self.kwargs['machine_pk'])
        form.instance.machine = machine
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('machine_detail', kwargs={'pk': self.kwargs['machine_pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = get_object_or_404(Machine, pk=self.kwargs['machine_pk'])
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        machine = get_object_or_404(Machine, pk=self.kwargs['machine_pk'])
        form.instance.machine = machine
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('machine_detail', kwargs={'pk': self.kwargs['machine_pk']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = get_object_or_404(Machine, pk=self.kwargs['machine_pk'])
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MaintenanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenances/maintenance_form.html'
    
    def test_func(self):
        user = self.request.user
        maintenance = self.get_object()
        
        is_client = user.groups.filter(name='Клиент').exists()
        is_service = user.groups.filter(name='Сервисная организация').exists()
        is_manager = user.is_superuser or user.groups.filter(name='Менеджер').exists()
        
        if is_manager:
            return True
        if is_client:
            return maintenance.machine.client == user
        if is_service:
            return maintenance.service_company.name == user.company_name
        return False
    
    def get_success_url(self):
        return reverse_lazy('machine_detail', kwargs={'pk': self.object.machine.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.get_object().machine
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_initial(self):
        initial = super().get_initial()
        obj = self.get_object()
        
        if obj.maintenance_date:
            initial['maintenance_date'] = obj.maintenance_date.strftime('%Y-%m-%d')
        if obj.work_order_date:
            initial['work_order_date'] = obj.work_order_date.strftime('%Y-%m-%d')
        
        return initial


class MaintenanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Maintenance
    template_name = 'maintenances/maintenance_confirm_delete.html'
    
    def test_func(self):
        user = self.request.user
        maintenance = self.get_object()
        
        is_client = user.groups.filter(name='Клиент').exists()
        is_service = user.groups.filter(name='Сервисная организация').exists()
        is_manager = user.is_superuser or user.groups.filter(name='Менеджер').exists()
        
        if is_manager:
            return True
        if is_client:
            return maintenance.machine.client == user
        if is_service:
            return maintenance.service_company.name == user.company_name
        return False
    
    def get_success_url(self):
        return reverse_lazy('machine_detail', kwargs={'pk': self.object.machine.pk})
    
class MaintenanceDetailView(LoginRequiredMixin, DetailView):
    model = Maintenance
    template_name = 'maintenances/maintenance_detail.html'
    context_object_name = 'maintenance'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Менеджер').exists():
            return Maintenance.objects.all()
        elif user.groups.filter(name='Клиент').exists():
            return Maintenance.objects.filter(machine__client=user)
        elif user.groups.filter(name='Сервисная организация').exists():
            return Maintenance.objects.filter(service_company__name=user.company_name)
        return Maintenance.objects.none()