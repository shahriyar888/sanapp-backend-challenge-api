from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'file_name', 'file_size', 
                  'content_type', 'uploaded_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'file_name', 'file_size', 'content_type', 
                           'uploaded_by', 'created_at', 'updated_at']


class DocumentUploadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    file = serializers.FileField()
