from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
        # token
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
         # users app
    path('users/', include('users.urls')),
        # empiloyees app
    path('employees/', include('employees.urls')),
        # work app
    path('work/', include('work.urls')),
        # finance app
    path('finance/', include('finance.urls')),
        # metrics app
    path('metrics/', include('metrics.urls')),
        # logs app
    path('logs/', include('logs.urls')),
    # docs
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
