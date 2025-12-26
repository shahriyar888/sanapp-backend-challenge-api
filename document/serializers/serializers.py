import base64
from rest_framework import serializers
from ..models import DocumentModel
from ..tasks import upload_document_to_minio


class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DocumentModel
        fields = ['id', 'title', 'description', 'file_name', 'file_size',
                  'content_type', 'status', 'error_message', 'uploaded_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'file_name', 'file_size', 'content_type', 'status',
                           'error_message', 'uploaded_by', 'created_at', 'updated_at']


class DocumentUploadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    file = serializers.FileField()

    def create(self, validated_data):
        file = validated_data['file']
        file_data = base64.b64encode(file.read()).decode('utf-8')

        document = DocumentModel.objects.create(
            title=validated_data['title'],
            description=validated_data.get('description', ''),
            file_name=file.name,
            file_size=file.size,
            content_type=file.content_type,
            status='PENDING',
            uploaded_by=self.context['user']
        )

        upload_document_to_minio.delay(
            document.id,
            file_data,
            file.name,
            file.size,
            file.content_type
        )

        return document

    def update(self, instance, validated_data):
        file = validated_data.get('file', None)
        if file:
            file_data = base64.b64encode(file.read()).decode('utf-8')
            instance.file_name = file.name
            instance.file_size = file.size
            instance.content_type = file.content_type
            instance.status = 'PENDING'
            instance.error_message = None
            instance.save()

            upload_document_to_minio.delay(
                instance.id,
                file_data,
                file.name,
                file.size,
                file.content_type
            )

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

