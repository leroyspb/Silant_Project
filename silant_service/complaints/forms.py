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
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        can_edit = user and (user.is_superuser or user.groups.filter(name='Менеджер').exists())
        
        if can_edit:
            self.fields['failure_node'].help_text = '<a href="/admin/reference_books/failurenode/add/" target="_blank" class="btn-add">➕ Добавить новый узел отказа</a>'
            self.fields['repair_method'].help_text = '<a href="/admin/reference_books/repairmethod/add/" target="_blank" class="btn-add">➕ Добавить новый способ восстановления</a>'
            self.fields['service_company'].help_text = '<a href="/admin/reference_books/servicecompany/add/" target="_blank" class="btn-add">➕ Добавить новую сервисную компанию</a>'