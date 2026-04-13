from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from machines.views import (
    MachineListView, MachineDetailView, search_machine,
    MaintenanceCreateView, ComplaintCreateView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('machines/', MachineListView.as_view(), name='machine_list'),
    path('machine/<int:pk>/', MachineDetailView.as_view(), name='machine_detail'),
    path('machine/<int:machine_pk>/maintenance/add/', MaintenanceCreateView.as_view(), name='add_maintenance'),
    path('machine/<int:machine_pk>/complaint/add/', ComplaintCreateView.as_view(), name='add_complaint'),
    path('search/', search_machine, name='search_machine'),
]