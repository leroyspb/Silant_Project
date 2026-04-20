from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Machine
from .forms import MachineForm  # ДОБАВИТЬ ЭТУ СТРОКУ
from maintenances.models import Maintenance
from complaints.models import Complaint
from maintenances.forms import MaintenanceForm
from complaints.forms import ComplaintForm
from reference_books.models import (
    TechniqueModel, EngineModel, TransmissionModel, 
    DriveAxleModel, SteerAxleModel,
)


# Проверка на менеджера
class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Менеджер').exists()

class MachineCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = Machine
    form_class = MachineForm  # используем форму вместо fields='__all__'
    template_name = 'machines/machine_form.html'
    
    def get_success_url(self):
        return reverse_lazy('machine_detail', kwargs={'pk': self.object.pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class MachineListView(LoginRequiredMixin, ListView):
    model = Machine
    template_name = 'machines/machine_list.html'
    context_object_name = 'machines'
    
    def get_queryset(self):
        user = self.request.user
        tab = self.request.GET.get('tab', 'machines')
        
        # Базовый queryset для машин
        if user.is_superuser or user.groups.filter(name='Менеджер').exists():
            machines_queryset = Machine.objects.all()
        elif user.groups.filter(name='Клиент').exists():
            machines_queryset = Machine.objects.filter(client=user)
        elif user.groups.filter(name='Сервисная организация').exists():
            machines_queryset = Machine.objects.filter(service_company__name=user.company_name)
        else:
            machines_queryset = Machine.objects.none()
        
        # Фильтрация для вкладки МАШИНЫ (только если активна вкладка машин)
        if tab == 'machines':
            technique = self.request.GET.get('technique_model')
            if technique:
                machines_queryset = machines_queryset.filter(technique_model_id=technique)
            
            engine = self.request.GET.get('engine_model')
            if engine:
                machines_queryset = machines_queryset.filter(engine_model_id=engine)
            
            transmission = self.request.GET.get('transmission_model')
            if transmission:
                machines_queryset = machines_queryset.filter(transmission_model_id=transmission)
            
            drive_axle = self.request.GET.get('drive_axle_model')
            if drive_axle:
                machines_queryset = machines_queryset.filter(drive_axle_model_id=drive_axle)
            
            steer_axle = self.request.GET.get('steer_axle_model')
            if steer_axle:
                machines_queryset = machines_queryset.filter(steer_axle_model_id=steer_axle)
        
        return machines_queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        tab = self.request.GET.get('tab', 'machines')
        
        # Получаем все машины для ТО и рекламаций (с учётом прав)
        if user.is_superuser or user.groups.filter(name='Менеджер').exists():
            machines_for_related = Machine.objects.all()
        elif user.groups.filter(name='Клиент').exists():
            machines_for_related = Machine.objects.filter(client=user)
        elif user.groups.filter(name='Сервисная организация').exists():
            machines_for_related = Machine.objects.filter(service_company__name=user.company_name)
        else:
            machines_for_related = Machine.objects.none()
        
        from maintenances.models import Maintenance
        from complaints.models import Complaint
        
        # Базовые queryset для ТО и рекламаций
        maintenances_qs = Maintenance.objects.filter(machine__in=machines_for_related)
        complaints_qs = Complaint.objects.filter(machine__in=machines_for_related)
        
        # ФИЛЬТРАЦИЯ ДЛЯ ТО (применяется всегда, независимо от активной вкладки)
        maintenance_type = self.request.GET.get('maintenance_type')
        if maintenance_type:
            maintenances_qs = maintenances_qs.filter(maintenance_type_id=maintenance_type)
        
        machine_number = self.request.GET.get('machine_number')
        if machine_number:
            maintenances_qs = maintenances_qs.filter(machine__factory_number__icontains=machine_number)
        
        service_company_to = self.request.GET.get('service_company_to')
        if service_company_to:
            maintenances_qs = maintenances_qs.filter(service_company_id=service_company_to)
        
        # ФИЛЬТРАЦИЯ ДЛЯ РЕКЛАМАЦИЙ (применяется всегда, независимо от активной вкладки)
        failure_node = self.request.GET.get('failure_node')
        if failure_node:
            complaints_qs = complaints_qs.filter(failure_node_id=failure_node)
        
        repair_method = self.request.GET.get('repair_method')
        if repair_method:
            complaints_qs = complaints_qs.filter(repair_method_id=repair_method)
        
        service_company_claim = self.request.GET.get('service_company_claim')
        if service_company_claim:
            complaints_qs = complaints_qs.filter(service_company_id=service_company_claim)
        
        context['maintenances'] = maintenances_qs.order_by('-maintenance_date')
        context['complaints'] = complaints_qs.order_by('-failure_date')
        
        # Данные для фильтров МАШИН
        from reference_books.models import (
            TechniqueModel, EngineModel, TransmissionModel, 
            DriveAxleModel, SteerAxleModel
        )
        
        context['technique_models'] = TechniqueModel.objects.all()
        context['engine_models'] = EngineModel.objects.all()
        context['transmission_models'] = TransmissionModel.objects.all()
        context['drive_axle_models'] = DriveAxleModel.objects.all()
        context['steer_axle_models'] = SteerAxleModel.objects.all()
        
        # Выбранные значения фильтров МАШИН
        context['selected_technique'] = self.request.GET.get('technique_model', '')
        context['selected_engine'] = self.request.GET.get('engine_model', '')
        context['selected_transmission'] = self.request.GET.get('transmission_model', '')
        context['selected_drive_axle'] = self.request.GET.get('drive_axle_model', '')
        context['selected_steer_axle'] = self.request.GET.get('steer_axle_model', '')
        
        # ДАННЫЕ ДЛЯ ФИЛЬТРОВ ТО И РЕКЛАМАЦИЙ
        from reference_books.models import MaintenanceType, ServiceCompany, FailureNode, RepairMethod
        
        context['maintenance_types'] = MaintenanceType.objects.all()
        context['service_companies'] = ServiceCompany.objects.all()
        context['failure_nodes'] = FailureNode.objects.all()
        context['repair_methods'] = RepairMethod.objects.all()
        
        # Выбранные значения фильтров для ТО
        context['selected_maintenance_type'] = self.request.GET.get('maintenance_type', '')
        context['selected_machine_number'] = self.request.GET.get('machine_number', '')
        context['selected_service_to'] = self.request.GET.get('service_company_to', '')
        
        # Выбранные значения фильтров для Рекламаций
        context['selected_failure_node'] = self.request.GET.get('failure_node', '')
        context['selected_repair_method'] = self.request.GET.get('repair_method', '')
        context['selected_service_claim'] = self.request.GET.get('service_company_claim', '')
        
        # Права
        is_client = user.groups.filter(name='Клиент').exists()
        is_service = user.groups.filter(name='Сервисная организация').exists()
        is_manager = user.is_superuser or user.groups.filter(name='Менеджер').exists()
        
        context['is_manager'] = is_manager
        context['is_service'] = is_service
        context['is_client'] = is_client
        context['can_add_maintenance'] = is_client or is_service or is_manager
        context['can_add_complaint'] = is_service or is_manager
        context['active_tab'] = tab
        
        return context


class MachineDetailView(LoginRequiredMixin, DetailView):
    model = Machine
    template_name = 'machines/machine_detail.html'
    context_object_name = 'machine'
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser or user.groups.filter(name='Менеджер').exists():
            return Machine.objects.all()
        elif user.groups.filter(name='Клиент').exists():
            return Machine.objects.filter(client=user)
        elif user.groups.filter(name='Сервисная организация').exists():
            return Machine.objects.filter(service_company__name=user.company_name)
        return Machine.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        machine = self.get_object()
        
        is_client = user.groups.filter(name='Клиент').exists()
        is_service = user.groups.filter(name='Сервисная организация').exists()
        is_manager = user.is_superuser or user.groups.filter(name='Менеджер').exists()
        
        context['is_manager'] = is_manager
        context['is_service'] = is_service
        context['is_client'] = is_client
        context['can_edit'] = is_service or is_manager
        context['can_add_maintenance'] = is_client or is_service or is_manager
        context['can_add_complaint'] = is_service or is_manager
       
        # Базовые queryset для ТО и рекламаций
        maintenances_qs = Maintenance.objects.filter(machine=machine)
        complaints_qs = Complaint.objects.filter(machine=machine)
        
        # ФИЛЬТРАЦИЯ ДЛЯ ТО
        maintenance_type = self.request.GET.get('maintenance_type')
        if maintenance_type:
            maintenances_qs = maintenances_qs.filter(maintenance_type_id=maintenance_type)
        
        organization = self.request.GET.get('organization')
        if organization:
            maintenances_qs = maintenances_qs.filter(organization_id=organization)
        
        # ФИЛЬТРАЦИЯ ДЛЯ РЕКЛАМАЦИЙ
        failure_node = self.request.GET.get('failure_node')
        if failure_node:
            complaints_qs = complaints_qs.filter(failure_node_id=failure_node)
        
        repair_method = self.request.GET.get('repair_method')
        if repair_method:
            complaints_qs = complaints_qs.filter(repair_method_id=repair_method)
        
        context['filtered_maintenances'] = maintenances_qs.order_by('-maintenance_date')
        context['filtered_complaints'] = complaints_qs.order_by('-failure_date')
        
        # Данные для фильтров
        from reference_books.models import MaintenanceType, ServiceCompany, FailureNode, RepairMethod
        context['maintenance_types'] = MaintenanceType.objects.all()
        context['organizations'] = ServiceCompany.objects.all()
        context['failure_nodes'] = FailureNode.objects.all()
        context['repair_methods'] = RepairMethod.objects.all()
        
        # Выбранные значения
        context['selected_maintenance_type'] = self.request.GET.get('maintenance_type', '')
        context['selected_organization'] = self.request.GET.get('organization', '')
        context['selected_failure_node'] = self.request.GET.get('failure_node', '')
        context['selected_repair_method'] = self.request.GET.get('repair_method', '')
        
        return context

class MachineUpdateView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    model = Machine
    form_class = MachineForm
    template_name = 'machines/machine_form.html'
    
    def get_success_url(self):
        return reverse_lazy('machine_detail', kwargs={'pk': self.object.pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MachineDeleteView(LoginRequiredMixin, ManagerRequiredMixin, DeleteView):
    model = Machine
    template_name = 'machines/machine_confirm_delete.html'
    success_url = reverse_lazy('machine_list')


class MaintenanceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenances/maintenance_form.html'
    permission_required = 'maintenances.add_maintenance'
    
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


class MaintenanceDeleteView(LoginRequiredMixin, ManagerRequiredMixin, DeleteView):
    model = Maintenance
    template_name = 'maintenances/maintenance_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('machine_detail', kwargs={'pk': self.object.machine.pk})


class ComplaintCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'complaints/complaint_form.html'
    permission_required = 'complaints.add_complaint'
    
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


class ComplaintUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'complaints/complaint_form.html'
    
    def test_func(self):
        user = self.request.user
        complaint = self.get_object()
        
        is_service = user.groups.filter(name='Сервисная организация').exists()
        is_manager = user.is_superuser or user.groups.filter(name='Менеджер').exists()
        
        if is_service:
            return complaint.service_company.name == user.company_name
        elif is_manager:
            return True
        return False
    
    def get_success_url(self):
        return reverse_lazy('machine_detail', kwargs={'pk': self.object.machine.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.get_object().machine
        return context


class ComplaintDeleteView(LoginRequiredMixin, ManagerRequiredMixin, DeleteView):
    model = Complaint
    template_name = 'complaints/complaint_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('machine_detail', kwargs={'pk': self.object.machine.pk})


def search_machine(request):
    factory_number = request.GET.get('factory_number')
    machine = None
    error = None
    
    if factory_number:
        try:
            machine = Machine.objects.get(factory_number=factory_number)
        except Machine.DoesNotExist:
            error = 'Данных о машине с таким заводским номером нет в системе'
    
    return render(request, 'search_result.html', {
        'machine': machine,
        'error': error,
    })

def home(request):
    # Если пользователь уже авторизован - перенаправляем на список машин
    if request.user.is_authenticated:
        return redirect('machine_list')
    
    factory_number = request.GET.get('factory_number')
    machine = None
    error = None
    
    if factory_number:
        try:
            machine = Machine.objects.get(factory_number=factory_number)
        except Machine.DoesNotExist:
            error = 'Данных о машине с таким заводским номером нет в системе'
    
    return render(request, 'home.html', {
        'machine': machine,
        'error': error,
        'factory_number': factory_number
    })