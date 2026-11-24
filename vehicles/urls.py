
from django.urls import path

from .views import (
    VehicleListCreateView,
    VehicleDetailView,
    VehicleEntryListCreateView,
    VehicleExitView,
    VehicleInsideView,
    DailyReportView
)

urlpatterns = [
    
    path('vehicles/', VehicleListCreateView.as_view(), name='vehicle-list'),
    path('vehicles/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    path('entries/', VehicleEntryListCreateView.as_view(), name='entry-list-create'),
    path('entries/<int:pk>/exit/', VehicleExitView.as_view(), name='vehicle-exit'),
    path('entries/inside/', VehicleInsideView.as_view(), name='vehicle-inside'),
    path('reports/daily/', DailyReportView.as_view(), name='daily-report'),
]
