from django.contrib import admin
from .models import Machine


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('factory_number', 'technique_model', 'client', 'service_company', 'shipping_date')
    list_filter = ('technique_model', 'client', 'service_company')
    search_fields = ('factory_number', 'client__username')