from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Machine
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
    fields = '__all__'
    template_name = 'machines/machine_form.html'
    
    def get_success_url(self):
        return reverse_lazy('machine_detail', kwargs={'pk': self.object.pk})

class MachineListView(LoginRequiredMixin, ListView):
    model = Machine
    template_name = 'machines/machine_list.html'
    context_object_name = 'machines'
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser or user.groups.filter(name='Менеджер').exists():
            queryset = Machine.objects.all()
        elif user.groups.filter(name='Клиент').exists():
            queryset = Machine.objects.filter(client=user)
        elif user.groups.filter(name='Сервисная организация').exists():
            queryset = Machine.objects.filter(service_company__name=user.company_name)
        else:
            queryset = Machine.objects.none()
        
        # Фильтрация
        technique = self.request.GET.get('technique_model')
        if technique:
            queryset = queryset.filter(technique_model_id=technique)
        
        engine = self.request.GET.get('engine_model')
        if engine:
            queryset = queryset.filter(engine_model_id=engine)
        
        transmission = self.request.GET.get('transmission_model')
        if transmission:
            queryset = queryset.filter(transmission_model_id=transmission)
        
        drive_axle = self.request.GET.get('drive_axle_model')
        if drive_axle:
            queryset = queryset.filter(drive_axle_model_id=drive_axle)
        
        steer_axle = self.request.GET.get('steer_axle_model')
        if steer_axle:
            queryset = queryset.filter(steer_axle_model_id=steer_axle)

        engine_number = self.request.GET.get('engine_number')
        if engine_number:
            queryset = queryset.filter(engine_number__icontains=engine_number)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        is_client = user.groups.filter(name='Клиент').exists()
        is_service = user.groups.filter(name='Сервисная организация').exists()
        is_manager = user.is_superuser or user.groups.filter(name='Менеджер').exists()
        
        context['can_add_maintenance'] = is_client or is_service or is_manager
        context['can_add_complaint'] = is_service or is_manager
        context['is_manager'] = is_manager
        context['is_client'] = is_client
        
        # Данные для фильтров
        context['technique_models'] = TechniqueModel.objects.all()
        context['engine_models'] = EngineModel.objects.all()
        context['transmission_models'] = TransmissionModel.objects.all()
        context['drive_axle_models'] = DriveAxleModel.objects.all()
        context['steer_axle_models'] = SteerAxleModel.objects.all()
        
        # Выбранные значения
        context['selected_technique'] = self.request.GET.get('technique_model', '')
        context['selected_engine'] = self.request.GET.get('engine_model', '')
        context['selected_transmission'] = self.request.GET.get('transmission_model', '')
        context['selected_drive_axle'] = self.request.GET.get('drive_axle_model', '')
        context['selected_steer_axle'] = self.request.GET.get('steer_axle_model', '')
        context['selected_engine_number'] = self.request.GET.get('engine_number', '')
        
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
        
        context['maintenances'] = Maintenance.objects.filter(machine=machine)
        context['complaints'] = Complaint.objects.filter(machine=machine)
        
        is_client = user.groups.filter(name='Клиент').exists()
        is_service = user.groups.filter(name='Сервисная организация').exists()
        is_manager = user.is_superuser or user.groups.filter(name='Менеджер').exists()
        
        context['can_add_maintenance'] = is_client or is_service or is_manager
        context['can_edit_maintenance'] = is_client or is_service or is_manager
        context['can_add_complaint'] = is_service or is_manager
        context['can_edit'] = is_service or is_manager
        context['is_manager'] = is_manager
        context['is_client'] = is_client
        
        return context


class MachineUpdateView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    model = Machine
    fields = '__all__'
    template_name = 'machines/machine_form.html'
    
    def get_success_url(self):
        return reverse_lazy('machine_detail', kwargs={'pk': self.object.pk})


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