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