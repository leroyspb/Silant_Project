from django.urls import path
from .views import (
    APIRootView,
    MachineListAPIView, MachineDetailAPIView,
    MaintenanceListAPIView, MaintenanceDetailAPIView,
    ComplaintListAPIView, ComplaintDetailAPIView
)

urlpatterns = [
    path('', APIRootView.as_view(), name='api_root'),
    path('machines/', MachineListAPIView.as_view(), name='api_machines'),
    path('machines/<int:pk>/', MachineDetailAPIView.as_view(), name='api_machine_detail'),
    path('maintenances/', MaintenanceListAPIView.as_view(), name='api_maintenances'),
    path('maintenances/<int:pk>/', MaintenanceDetailAPIView.as_view(), name='api_maintenance_detail'),
    path('complaints/', ComplaintListAPIView.as_view(), name='api_complaints'),
    path('complaints/<int:pk>/', ComplaintDetailAPIView.as_view(), name='api_complaint_detail'),
]