from rest_framework import serializers
from .models import DocumentModel
from .storage import MinIOStorage


class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DocumentModel
        fields = ['id', 'title', 'description', 'file_name', 'file_size',
                  'content_type', 'uploaded_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'file_name', 'file_size', 'content_type',
                           'uploaded_by', 'created_at', 'updated_at']


class DocumentUploadSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    file = serializers.FileField()

    def create(self, validated_data):
        file = validated_data['file']
        storage = MinIOStorage()

        file_path = storage.upload_file(file, file.name)

        document = DocumentModel.objects.create(
            title=validated_data['title'],
            description=validated_data.get('description', ''),
            file_name=file.name,
            file_path=file_path,
            file_size=file.size,
            content_type=file.content_type,
            uploaded_by=self.context['user']
        )
        return document

    def update(self, instance, validated_data):
        file = validated_data.get('file', None)
        if file:
            storage = MinIOStorage()
            file_path = storage.upload_file(file, file.name)
            instance.file_name = file.name
            instance.file_path = file_path
            instance.file_size = file.size
            instance.content_type = file.content_type

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

