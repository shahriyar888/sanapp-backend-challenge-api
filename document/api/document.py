from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import DocumentModel
from ..permisions import DocumentPermissions
from ..serializers import DocumentSerializer, DocumentUploadSerializer
from ..docs.swagger_schemas import (
    DOCUMENT_FORM_PARAMS,
    DOCUMENT_PARTIAL_FORM_PARAMS,
    DOCUMENT_RESPONSES,
    DOCUMENT_CREATE_RESPONSES,
    DOCUMENT_DELETE_RESPONSES
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
        'destroy':['admin']
    }

    def get_queryset(self):
        search_param = self.request.query_params.get('s', '')
        if search_param:
            return DocumentModel.objects.search(s=search_param)
        return DocumentModel.objects.all()

    def get_parsers(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
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

    @swagger_auto_schema(
        operation_description="List all documents with optional search",
        manual_parameters=[
            openapi.Parameter(
                's',
                openapi.IN_QUERY,
                description="Search term to filter documents by title, description, or filename",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={200: DocumentSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a document by ID",
        responses={200: DocumentSerializer(), 404: "Not found"}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Upload a new document",
        manual_parameters=DOCUMENT_FORM_PARAMS,
        responses=DOCUMENT_CREATE_RESPONSES
    )
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

    @swagger_auto_schema(
        operation_description="Update a document (full update)",
        manual_parameters=DOCUMENT_FORM_PARAMS,
        responses=DOCUMENT_RESPONSES
    )
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

    @swagger_auto_schema(
        operation_description="Partially update a document",
        manual_parameters=DOCUMENT_PARTIAL_FORM_PARAMS,
        responses=DOCUMENT_RESPONSES
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a document",
        responses=DOCUMENT_DELETE_RESPONSES
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
