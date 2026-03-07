from django.contrib import admin
from .models import Log

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'action')
    ordering = ('-created_at',)
