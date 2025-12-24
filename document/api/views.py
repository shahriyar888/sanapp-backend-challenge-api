from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models import Document
from ..serializers import DocumentSerializer, DocumentUploadSerializer
from ..storage import MinIOStorage


class DocumentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_parsers(self):
        if self.request.method == 'POST':
            return [MultiPartParser(), FormParser()]
        return super().get_parsers()

    @swagger_auto_schema(
        responses={200: DocumentSerializer(many=True)}
    )
    def get(self, request):
        documents = Document.objects.filter(uploaded_by=request.user)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=None,
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('description', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True),
        ],
        responses={201: DocumentSerializer}
    )
    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            storage = MinIOStorage()
            
            file_path = storage.upload_file(file, file.name)
            
            document = Document.objects.create(
                title=serializer.validated_data['title'],
                description=serializer.validated_data.get('description', ''),
                file_name=file.name,
                file_path=file_path,
                file_size=file.size,
                content_type=file.content_type,
                uploaded_by=request.user
            )
            
            return Response(
                DocumentSerializer(document).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Document.objects.get(pk=pk, uploaded_by=user)
        except Document.DoesNotExist:
            return None

    @swagger_auto_schema(
        responses={200: DocumentSerializer}
    )
    def get(self, request, pk):
        document = self.get_object(pk, request.user)
        if not document:
            return Response(
                {'error': 'Document not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        storage = MinIOStorage()
        download_url = storage.get_file_url(document.file_path)
        
        data = DocumentSerializer(document).data
        data['download_url'] = download_url
        return Response(data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={200: DocumentSerializer}
    )
    def patch(self, request, pk):
        document = self.get_object(pk, request.user)
        if not document:
            return Response(
                {'error': 'Document not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = DocumentSerializer(document, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: 'Document deleted'}
    )
    def delete(self, request, pk):
        document = self.get_object(pk, request.user)
        if not document:
            return Response(
                {'error': 'Document not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        storage = MinIOStorage()
        storage.delete_file(document.file_path)
        document.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
