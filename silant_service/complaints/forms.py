from django import forms
from .models import Complaint
from reference_books.models import ServiceCompany

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['failure_date', 'operating_hours', 'failure_node', 
                  'failure_description', 'repair_method', 'used_parts', 'recovery_date', 'service_company']
        widgets = {
            'failure_date': forms.DateInput(attrs={'type': 'date'}),
            'recovery_date': forms.DateInput(attrs={'type': 'date'}),
            'failure_description': forms.Textarea(attrs={'rows': 3}),
            'used_parts': forms.Textarea(attrs={'rows': 2}),
        }