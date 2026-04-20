from django import forms
from .models import Machine
from reference_books.models import (
    TechniqueModel, EngineModel, TransmissionModel,
    DriveAxleModel, SteerAxleModel, ServiceCompany
)


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = '__all__'
        widgets = {
            'shipping_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_address': forms.Textarea(attrs={'rows': 2}),
            'equipment': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Проверяем, может ли пользователь редактировать справочники (только менеджер)
        can_edit = user and (user.is_superuser or user.groups.filter(name='Менеджер').exists())
        
        if can_edit:
            # Кнопки для добавления новых справочников
            self.fields['technique_model'].help_text = '<a href="/admin/reference_books/techniquemodel/add/" target="_blank" class="btn-add-reference">➕ Добавить новую модель техники</a>'
            self.fields['engine_model'].help_text = '<a href="/admin/reference_books/enginemodel/add/" target="_blank" class="btn-add-reference">➕ Добавить новую модель двигателя</a>'
            self.fields['transmission_model'].help_text = '<a href="/admin/reference_books/transmissionmodel/add/" target="_blank" class="btn-add-reference">➕ Добавить новую модель трансмиссии</a>'
            self.fields['drive_axle_model'].help_text = '<a href="/admin/reference_books/driveaxlemodel/add/" target="_blank" class="btn-add-reference">➕ Добавить новую модель ведущего моста</a>'
            self.fields['steer_axle_model'].help_text = '<a href="/admin/reference_books/steeraxlemodel/add/" target="_blank" class="btn-add-reference">➕ Добавить новую модель управляемого моста</a>'
            self.fields['service_company'].help_text = '<a href="/admin/reference_books/servicecompany/add/" target="_blank" class="btn-add-reference">➕ Добавить новую сервисную компанию</a>'