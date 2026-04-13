from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Machine
from .forms import MachineForm

User = get_user_model()

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    form = MachineForm
    list_display = ('factory_number', 'technique_model', 'client', 'service_company', 'shipping_date')
    list_filter = ('technique_model', 'client', 'service_company')
    search_fields = ('factory_number', 'client__username', 'client__company_name')