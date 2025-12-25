from django.urls import path
from .api import DocumentViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'documents', DocumentViewSet, basename='document')
urlpatterns = router.urls
