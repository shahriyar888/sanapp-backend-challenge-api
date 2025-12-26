from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.openapi import OpenApiTypes
from ..serializers import DocumentSerializer

# Schema definitions for document endpoints
LIST_SCHEMA = extend_schema(
    description="List all documents with optional search",
    parameters=[
        OpenApiParameter(
            's',
            OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Search term to filter documents by title, description, or filename",
            required=False
        )
    ],
    responses={200: DocumentSerializer(many=True)}
)

RETRIEVE_SCHEMA = extend_schema(
    description="Retrieve a document by ID",
    responses={200: DocumentSerializer, 404: None}
)

CREATE_SCHEMA = extend_schema(
    description="Upload a new document",
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'title': {'type': 'string'},
                'description': {'type': 'string'},
                'file': {'type': 'string', 'format': 'binary'}
            },
            'required': ['title', 'file']
        }
    },
    responses={201: DocumentSerializer, 400: None}
)

UPDATE_SCHEMA = extend_schema(
    description="Update a document (full update)",
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'title': {'type': 'string'},
                'description': {'type': 'string'},
                'file': {'type': 'string', 'format': 'binary'}
            },
            'required': ['title', 'file']
        }
    },
    responses={200: DocumentSerializer, 400: None, 404: None}
)

PARTIAL_UPDATE_SCHEMA = extend_schema(
    description="Partially update a document",
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'title': {'type': 'string'},
                'description': {'type': 'string'},
                'file': {'type': 'string', 'format': 'binary'}
            }
        }
    },
    responses={200: DocumentSerializer, 400: None, 404: None}
)

DESTROY_SCHEMA = extend_schema(
    description="Delete a document",
    responses={204: None, 404: None}
)
