from django import forms
from .models import Maintenance
from reference_books.models import MaintenanceType, ServiceCompany


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['maintenance_type', 'maintenance_date', 'operating_hours', 
                  'work_order_number', 'work_order_date', 'organization', 'service_company']
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}, format='%Y-%m-%d'),
            'work_order_date': forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}, format='%Y-%m-%d'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если есть данные, преобразуем даты в нужный формат
        if self.instance and self.instance.pk:
            if self.instance.maintenance_date:
                self.initial['maintenance_date'] = self.instance.maintenance_date.strftime('%Y-%m-%d')
            if self.instance.work_order_date:
                self.initial['work_order_date'] = self.instance.work_order_date.strftime('%Y-%m-%d')