from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmployeeListCreateView.as_view(), name='employee-list'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('me/', views.MyEmployeeProfileView.as_view(), name='my-employee-profile'),
    path('<int:pk>/fire/', views.FireEmployeeView.as_view(), name='fire-employee'),
]