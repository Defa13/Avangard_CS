from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name', 
        'last_name', 
        'position', 
        'department', 
        'status', 
        'base_salary', 
        'manager', 
        'hire_date', 
        'fired_date'
    )
    search_fields = ('first_name', 'last_name', 'position', 'department')
    list_filter = ('status', 'department', 'hire_date')
    ordering = ('last_name', 'first_name')