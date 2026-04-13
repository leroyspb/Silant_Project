from django.contrib import admin
from .models import Maintenance

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('machine', 'maintenance_type', 'maintenance_date', 'operating_hours')
    list_filter = ('maintenance_type', 'service_company')
    search_fields = ('machine__factory_number',)