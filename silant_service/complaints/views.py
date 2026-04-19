from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Complaint
from .forms import ComplaintForm
from reference_books.models import FailureNode, RepairMethod, ServiceCompany
from machines.models import Machine


class ComplaintListView(LoginRequiredMixin, ListView):
    model = Complaint
    template_name = 'complaints/complaint_list.html'
    context_object_name = 'complaints'
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser or user.groups.filter(name='Менеджер').exists():
            queryset = Complaint.objects.all()
        elif user.groups.filter(name='Клиент').exists():
            queryset = Complaint.objects.filter(machine__client=user)
        elif user.groups.filter(name='Сервисная организация').exists():
            queryset = Complaint.objects.filter(service_company__name=user.company_name)
        else:
            queryset = Complaint.objects.none()
        
        # Фильтрация
        failure_node = self.request.GET.get('failure_node')
        if failure_node:
            queryset = queryset.filter(failure_node_id=failure_node)
        
        repair_method = self.request.GET.get('repair_method')
        if repair_method:
            queryset = queryset.filter(repair_method_id=repair_method)
        
        service_company = self.request.GET.get('service_company')
        if service_company:
            queryset = queryset.filter(service_company_id=service_company)
        
        return queryset.order_by('-failure_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['failure_nodes'] = FailureNode.objects.all()
        context['repair_methods'] = RepairMethod.objects.all()
        context['service_companies'] = ServiceCompany.objects.all()
        
        context['selected_failure_node'] = self.request.GET.get('failure_node', '')
        context['selected_repair_method'] = self.request.GET.get('repair_method', '')
        context['selected_service'] = self.request.GET.get('service_company', '')
        
        context['is_manager'] = user.is_superuser or user.groups.filter(name='Менеджер').exists()
        context['is_service'] = user.groups.filter(name='Сервисная организация').exists()
        
        return context


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
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ComplaintUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = 'complaints/complaint_form.html'
    
    def test_func(self):
        user = self.request.user
        complaint = self.get_object()
        
        is_service = user.groups.filter(name='Сервисная организация').exists()
        is_manager = user.is_superuser or user.groups.filter(name='Менеджер').exists()
        
        if is_manager:
            return True
        if is_service:
            return complaint.service_company.name == user.company_name
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
        
        if obj.failure_date:
            initial['failure_date'] = obj.failure_date.strftime('%Y-%m-%d')
        if obj.recovery_date:
            initial['recovery_date'] = obj.recovery_date.strftime('%Y-%m-%d')
        
        return initial


class ComplaintDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Complaint
    template_name = 'complaints/complaint_confirm_delete.html'
    
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='Менеджер').exists()
    
    def get_success_url(self):
        return reverse_lazy('complaint_list')
    

class ComplaintDetailView(LoginRequiredMixin, DetailView):
    model = Complaint
    template_name = 'complaints/complaint_detail.html'
    context_object_name = 'complaint'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Менеджер').exists():
            return Complaint.objects.all()
        elif user.groups.filter(name='Клиент').exists():
            return Complaint.objects.filter(machine__client=user)
        elif user.groups.filter(name='Сервисная организация').exists():
            return Complaint.objects.filter(service_company__name=user.company_name)
        return Complaint.objects.none()