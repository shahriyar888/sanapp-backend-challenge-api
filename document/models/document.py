from django.db import models
from django.contrib.auth.models import User

from sannap_project.abstarct_models import BaseModel


class DocumentModel(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    file_size = models.BigIntegerField()
    content_type = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
