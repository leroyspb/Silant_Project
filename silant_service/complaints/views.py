from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Complaint
from reference_books.models import FailureNode, RepairMethod, ServiceCompany


class ComplaintListView(LoginRequiredMixin, ListView):
    model = Complaint
    template_name = 'complaints/complaint_list.html'
    context_object_name = 'complaints'
    
    def get_queryset(self):
        user = self.request.user
        
        # Базовый queryset в зависимости от роли
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
            queryset = queryset.filter(failure_node__icontains=failure_node)
        
        repair_method = self.request.GET.get('repair_method')
        if repair_method:
            queryset = queryset.filter(repair_method__icontains=repair_method)
        
        service_company = self.request.GET.get('service_company')
        if service_company:
            queryset = queryset.filter(service_company_id=service_company)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Данные для фильтров
        context['failure_nodes'] = FailureNode.objects.all()
        context['repair_methods'] = RepairMethod.objects.all()
        context['service_companies'] = ServiceCompany.objects.all()
        
        # Выбранные значения
        context['selected_failure_node'] = self.request.GET.get('failure_node', '')
        context['selected_repair_method'] = self.request.GET.get('repair_method', '')
        context['selected_service'] = self.request.GET.get('service_company', '')
        
        return context


class ComplaintUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Complaint
    fields = ['failure_date', 'operating_hours', 'failure_node', 
              'failure_description', 'repair_method', 'used_parts', 
              'recovery_date', 'service_company']
    template_name = 'complaints/complaint_form.html'
    
    def test_func(self):
        user = self.request.user
        complaint = self.get_object()
        return (user.is_superuser or 
                user.groups.filter(name='Менеджер').exists() or
                (user.groups.filter(name='Сервисная организация').exists() and 
                 complaint.service_company.name == user.company_name))
    
    def get_success_url(self):
        return reverse_lazy('machine_detail', kwargs={'pk': self.object.machine.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['machine'] = self.object.machine
        return context