from django.contrib import admin
from .models import DocumentModel


@admin.register(DocumentModel)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'file_name', 'uploaded_by', 'created_at']
    list_filter = ['created_at', 'uploaded_by']
    search_fields = ['title', 'description', 'file_name']
    readonly_fields = ['created_at', 'updated_at']
