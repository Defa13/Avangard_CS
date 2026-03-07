from django.urls import path
from . import views

urlpatterns = [
    path('', views.WorkListCreateView.as_view(), name='work-list-create'),
    path('<int:pk>/', views.WorkDetailView.as_view(), name='work-detail'),
    path('my-shifts/', views.MyWorkShiftListView.as_view(), name='my-work-shifts'),
]
