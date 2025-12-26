from django.contrib.auth import get_user_model
from django.db import models

from document.managers.document import DocumentManager
from sannap_project.abstarct_models import BaseModel

User=get_user_model()

class DocumentModel(BaseModel):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500, blank=True, null=True)
    file_size = models.BigIntegerField()
    content_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    error_message = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')

    objects = DocumentManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
