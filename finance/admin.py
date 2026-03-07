from django.contrib import admin
from .models import Payroll

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'employee',
        'period_start',
        'period_end',
        'total_amount',
        'is_paid',
        'paid_at',
        'created_at',
        'updated_at'
    )
    list_filter = ('is_paid', 'period_start', 'period_end')
    search_fields = ('employee__first_name', 'employee__last_name')
    readonly_fields = ('created_at', 'updated_at', 'total_amount', 'worked_hours', 'base_salary')
