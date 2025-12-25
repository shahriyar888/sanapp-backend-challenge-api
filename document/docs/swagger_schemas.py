from drf_yasg import openapi
from ..serializers import DocumentSerializer

# Form parameters
DOCUMENT_FORM_PARAMS = [
    openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
    openapi.Parameter('description', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
    openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, required=True),
]

DOCUMENT_PARTIAL_FORM_PARAMS = [
    openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
    openapi.Parameter('description', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
    openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False),
]

# Responses
DOCUMENT_RESPONSES = {
    200: DocumentSerializer(),
    400: "Bad request",
    404: "Not found"
}

DOCUMENT_CREATE_RESPONSES = {
    201: DocumentSerializer(),
    400: "Bad request"
}

DOCUMENT_DELETE_RESPONSES = {
    204: "No content",
    404: "Not found"
}
