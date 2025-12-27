from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from django.http import HttpResponse
from ..models import DocumentModel
from ..permisions import DocumentPermissions
from ..serializers import DocumentSerializer, DocumentUploadSerializer
from ..storage import MinIOStorage
from ..docs.swagger_schemas import (
    LIST_SCHEMA,
    RETRIEVE_SCHEMA,
    CREATE_SCHEMA,
    UPDATE_SCHEMA,
    PARTIAL_UPDATE_SCHEMA,
    DESTROY_SCHEMA
)


class DocumentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated,DocumentPermissions]
    model = DocumentModel
    queryset = DocumentModel.objects.all()
    action_roles={
        'list':['admin','editor','viewer'],
        'retrieve':['admin','editor','viewer'],
        'create':['admin','editor'],
        'update':['admin','editor'],
        'partial_update':['admin','editor'],
        'destroy':['admin'],
        'status':['admin','editor','viewer'],
        'download':['admin','editor','viewer']
    }

    def get_queryset(self):
        search_param = self.request.query_params.get('s', '')
        if search_param:
            return DocumentModel.objects.search(s=search_param)
        return DocumentModel.objects.all()

    def get_parsers(self):
        if hasattr(self, 'request') and self.request and self.request.method in ['POST', 'PUT', 'PATCH']:
            return [MultiPartParser(), FormParser()]
        return super().get_parsers()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return DocumentUploadSerializer
        return DocumentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    @LIST_SCHEMA
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @RETRIEVE_SCHEMA
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @CREATE_SCHEMA
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        document = serializer.save()
        output_serializer = DocumentSerializer(document)
        headers = self.get_success_headers(output_serializer.data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @UPDATE_SCHEMA
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        document = serializer.save()
        output_serializer = DocumentSerializer(document)
        return Response(output_serializer.data)

    @PARTIAL_UPDATE_SCHEMA
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @DESTROY_SCHEMA
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        document = self.get_object()
        return Response({
            'id': document.id,
            'status': document.status,
            'error_message': document.error_message
        })

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        document = self.get_object()
        storage = MinIOStorage()
        file_url = storage.get_file_url(document.file_path)
        return Response({'download_url': file_url})
