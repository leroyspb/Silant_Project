from django import forms
from .models import Complaint
from reference_books.models import ServiceCompany


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['failure_date', 'operating_hours', 'failure_node', 
                  'failure_description', 'repair_method', 'used_parts', 
                  'recovery_date', 'service_company']
        widgets = {
            'failure_date': forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}, format='%Y-%m-%d'),
            'recovery_date': forms.DateInput(attrs={'type': 'date', 'class': 'date-input'}, format='%Y-%m-%d'),
            'failure_description': forms.Textarea(attrs={'rows': 3, 'class': 'textarea-field'}),
            'used_parts': forms.Textarea(attrs={'rows': 2, 'class': 'textarea-field'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если есть данные, преобразуем даты в нужный формат
        if self.instance and self.instance.pk:
            if self.instance.failure_date:
                self.initial['failure_date'] = self.instance.failure_date.strftime('%Y-%m-%d')
            if self.instance.recovery_date:
                self.initial['recovery_date'] = self.instance.recovery_date.strftime('%Y-%m-%d')