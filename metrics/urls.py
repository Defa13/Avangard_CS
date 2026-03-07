from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmployeeMetricsListCreateView.as_view(), name='metrics'),
    path('<int:pk>/', views.EmployeeMetricsDetailView.as_view(), name='metrics-detail'),
    path('export/', views.EmployeeMetricsExportExcelView.as_view(), name='metrics-export'),
]
