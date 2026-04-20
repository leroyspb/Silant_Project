from rest_framework import serializers
from machines.models import Machine
from maintenances.models import Maintenance
from complaints.models import Complaint
from reference_books.models import (
    TechniqueModel, EngineModel, TransmissionModel,
    DriveAxleModel, SteerAxleModel, ServiceCompany,
    MaintenanceType, FailureNode, RepairMethod
)


class TechniqueModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechniqueModel
        fields = ['id', 'name', 'description']


class EngineModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineModel
        fields = ['id', 'name', 'description']


class TransmissionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmissionModel
        fields = ['id', 'name', 'description']


class DriveAxleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveAxleModel
        fields = ['id', 'name', 'description']


class SteerAxleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteerAxleModel
        fields = ['id', 'name', 'description']


class ServiceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCompany
        fields = ['id', 'name', 'description']


class MaintenanceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceType
        fields = ['id', 'name', 'description']


class FailureNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FailureNode
        fields = ['id', 'name', 'description']


class RepairMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairMethod
        fields = ['id', 'name', 'description']


class MachineSerializer(serializers.ModelSerializer):
    technique_model = TechniqueModelSerializer(read_only=True)
    engine_model = EngineModelSerializer(read_only=True)
    transmission_model = TransmissionModelSerializer(read_only=True)
    drive_axle_model = DriveAxleModelSerializer(read_only=True)
    steer_axle_model = SteerAxleModelSerializer(read_only=True)
    service_company = ServiceCompanySerializer(read_only=True)
    client_name = serializers.CharField(source='client.username', read_only=True)
    
    class Meta:
        model = Machine
        fields = [
            'id', 'factory_number', 'technique_model', 'engine_model',
            'engine_number', 'transmission_model', 'transmission_number',
            'drive_axle_model', 'drive_axle_number', 'steer_axle_model',
            'steer_axle_number', 'supply_contract', 'shipping_date',
            'consignee', 'delivery_address', 'equipment', 'client_name',
            'service_company'
        ]


class MaintenanceSerializer(serializers.ModelSerializer):
    maintenance_type = MaintenanceTypeSerializer(read_only=True)
    organization = ServiceCompanySerializer(read_only=True)
    service_company = ServiceCompanySerializer(read_only=True)
    machine_number = serializers.CharField(source='machine.factory_number', read_only=True)
    
    class Meta:
        model = Maintenance
        fields = [
            'id', 'machine_number', 'maintenance_type', 'maintenance_date',
            'operating_hours', 'work_order_number', 'work_order_date',
            'organization', 'service_company'
        ]


class ComplaintSerializer(serializers.ModelSerializer):
    failure_node = FailureNodeSerializer(read_only=True)
    repair_method = RepairMethodSerializer(read_only=True)
    service_company = ServiceCompanySerializer(read_only=True)
    machine_number = serializers.CharField(source='machine.factory_number', read_only=True)
    
    class Meta:
        model = Complaint
        fields = [
            'id', 'machine_number', 'failure_date', 'operating_hours',
            'failure_node', 'failure_description', 'repair_method',
            'used_parts', 'recovery_date', 'downtime', 'service_company'
        ]