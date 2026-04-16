from django import forms
from .models import Maintenance
from reference_books.models import MaintenanceType, ServiceCompany

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['maintenance_type', 'maintenance_date', 'operating_hours', 
                  'work_order_number', 'work_order_date', 'organization', 'service_company']
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
            'work_order_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        can_edit = user and (user.is_superuser or user.groups.filter(name='Менеджер').exists())
        
        if can_edit:
            self.fields['maintenance_type'].help_text = '<a href="/admin/reference_books/maintenancetype/add/" target="_blank" class="btn-add">➕ Добавить новый вид ТО</a>'
            self.fields['organization'].help_text = '<a href="/admin/reference_books/servicecompany/add/" target="_blank" class="btn-add">➕ Добавить новую организацию</a>'
            self.fields['service_company'].help_text = '<a href="/admin/reference_books/servicecompany/add/" target="_blank" class="btn-add">➕ Добавить новую сервисную компанию</a>'