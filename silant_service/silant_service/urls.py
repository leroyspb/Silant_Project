from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from machines.views import (
    MachineListView, MachineDetailView, MachineUpdateView, MachineDeleteView,
    search_machine, MaintenanceCreateView, MaintenanceUpdateView, MaintenanceDeleteView,
    ComplaintCreateView, ComplaintUpdateView, ComplaintDeleteView
)
from maintenances.views import MaintenanceListView
from complaints.views import ComplaintListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('machines/', MachineListView.as_view(), name='machine_list'),
    path('machine/<int:pk>/', MachineDetailView.as_view(), name='machine_detail'),
    path('machine/<int:pk>/edit/', MachineUpdateView.as_view(), name='machine_edit'),
    path('machine/<int:pk>/delete/', MachineDeleteView.as_view(), name='machine_delete'),
    path('machine/<int:machine_pk>/maintenance/add/', MaintenanceCreateView.as_view(), name='add_maintenance'),
    path('maintenance/<int:pk>/edit/', MaintenanceUpdateView.as_view(), name='maintenance_edit'),
    path('maintenance/<int:pk>/delete/', MaintenanceDeleteView.as_view(), name='maintenance_delete'),
    path('machine/<int:machine_pk>/complaint/add/', ComplaintCreateView.as_view(), name='add_complaint'),
    path('complaint/<int:pk>/edit/', ComplaintUpdateView.as_view(), name='complaint_edit'),
    path('complaint/<int:pk>/delete/', ComplaintDeleteView.as_view(), name='complaint_delete'),
    path('maintenances/', MaintenanceListView.as_view(), name='maintenance_list'),
    path('complaints/', ComplaintListView.as_view(), name='complaint_list'),
    path('search/', search_machine, name='search_machine'),
]