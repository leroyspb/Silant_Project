from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Machine
from maintenances.models import Maintenance
from complaints.models import Complaint
from maintenances.forms import MaintenanceForm
from complaints.forms import ComplaintForm


class MachineListView(LoginRequiredMixin, ListView):
    model = Machine
    template_name = 'machines/machine_list.html'
    context_object_name = 'machines'
    
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
        
        # Права на добавление ТО и рекламаций
        context['can_add_maintenance'] = (
            user.has_perm('maintenances.add_maintenance') or 
            user.groups.filter(name='Сервисная организация').exists() or
            user.groups.filter(name='Менеджер').exists()
        )
        context['can_add_complaint'] = (
            user.has_perm('complaints.add_complaint') or 
            user.groups.filter(name='Сервисная организация').exists() or
            user.groups.filter(name='Менеджер').exists()
        )
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
        
        # Получаем ТО и рекламации для этой машины
        context['maintenances'] = Maintenance.objects.filter(machine=self.object)
        context['complaints'] = Complaint.objects.filter(machine=self.object)
        
        # Права
        context['can_add_maintenance'] = (
            user.has_perm('maintenances.add_maintenance') or 
            user.groups.filter(name='Сервисная организация').exists() or
            user.groups.filter(name='Менеджер').exists()
        )
        context['can_add_complaint'] = (
            user.has_perm('complaints.add_complaint') or 
            user.groups.filter(name='Сервисная организация').exists() or
            user.groups.filter(name='Менеджер').exists()
        )
        context['can_edit'] = (
            user.groups.filter(name='Сервисная организация').exists() or
            user.groups.filter(name='Менеджер').exists() or
            user.is_superuser
        )
        return context


# Добавление ТО
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


# Добавление рекламации
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