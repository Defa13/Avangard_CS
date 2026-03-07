from django.urls import path
from . import views 

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('users/', views.UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/me/', views.MeView.as_view(), name='me'),
    path('users/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('users/deactivate/<int:user_id>/', views.DeactivateUserView.as_view(), name='deactivate-user'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
