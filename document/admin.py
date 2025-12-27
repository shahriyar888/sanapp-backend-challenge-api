from django.contrib import admin
from auditlog.admin import LogEntryAdmin
from auditlog.models import LogEntry
from auditlog.registry import auditlog
from .models import DocumentModel


@admin.register(DocumentModel)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'file_name', 'uploaded_by', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'uploaded_by']
    search_fields = ['title', 'description', 'file_name']
    readonly_fields = ['created_at', 'updated_at']


auditlog.register(DocumentModel)
