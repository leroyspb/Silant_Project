from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('machine', 'failure_date', 'failure_node', 'recovery_date', 'downtime')
    list_filter = ('failure_node', 'repair_method', 'service_company')
    search_fields = ('machine__factory_number',)
    
    def downtime(self, obj):
        return obj.downtime
    downtime.short_description = 'Время простоя (дни)'