from django.urls import path
from . import views

urlpatterns = [
    path('', views.PayrollListCreateView.as_view(), name='payroll-list-create'),
    path('<int:pk>/', views.PayrollDetailView.as_view(), name='payroll-detail'),
    path('<int:pk>/pay/', views.PayrollPayView.as_view(), name='payroll-pay'),
    path('my-payrolls/', views.MyPayrollListView.as_view(), name='my-payrolls'),
    path('export-excel/', views.PayrollExportExcelView.as_view(), name='payroll-export-excel'),
]
