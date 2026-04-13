from django import forms
from django.contrib.auth import get_user_model
from .models import Machine

User = get_user_model()

class MachineForm(forms.ModelForm):
    client = forms.ModelChoiceField(
        queryset=User.objects.filter(role='client'),
        label='Клиент',
        empty_label="Выберите клиента"
    )
    
    class Meta:
        model = Machine
        fields = '__all__'