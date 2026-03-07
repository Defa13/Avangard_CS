from django.contrib import admin
from .models import EmployeeMetrics

@admin.register(EmployeeMetrics)
class EmployeeMetricsAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'period', 'quality', 'breaks_pct', 'cvd', 'hold_pct', 'created_at')
    list_filter = ('period', 'employee')
    search_fields = ('employee__full_name',)
    ordering = ('-period',)
