from django.contrib import admin
from .models import WorkShift

@admin.register(WorkShift)
class WorkShiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'date', 'start_time', 'end_time', 'hours_worked', 'day_type')
    list_filter = ('day_type', 'date')
    search_fields = ('employee__first_name', 'employee__last_name')
    ordering = ('-date',)
