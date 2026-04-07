from django.contrib import admin
from .models import (
    TechniqueModel, EngineModel, TransmissionModel,
    DriveAxleModel, SteerAxleModel, MaintenanceType,
    FailureNode, RepairMethod, ServiceCompany
)


@admin.register(TechniqueModel, EngineModel, TransmissionModel,
                DriveAxleModel, SteerAxleModel, MaintenanceType,
                FailureNode, RepairMethod, ServiceCompany)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)