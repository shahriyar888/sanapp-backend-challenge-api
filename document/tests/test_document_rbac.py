import pytest
from django.urls import reverse
from unittest.mock import patch, MagicMock
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestDocumentRBAC:
    
    def test_admin_can_list_documents(self, admin_client, document):
        url = reverse('document-list')
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_editor_can_list_documents(self, editor_client, document):
        url = reverse('document-list')
        response = editor_client.get(url)
        assert response.status_code == 200

    def test_viewer_can_list_documents(self, viewer_client, document):
        url = reverse('document-list')
        response = viewer_client.get(url)
        assert response.status_code == 200

    def test_admin_can_retrieve_document(self, admin_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_editor_can_retrieve_document(self, editor_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        response = editor_client.get(url)
        assert response.status_code == 200

    def test_viewer_can_retrieve_document(self, viewer_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        response = viewer_client.get(url)
        assert response.status_code == 200

    @patch('document.serializers.serializers.MinIOStorage')
    def test_admin_can_create_document(self, mock_storage, admin_client):
        mock_storage_instance = MagicMock()
        mock_storage_instance.upload_file.return_value = 'documents/test.pdf'
        mock_storage.return_value = mock_storage_instance
        
        url = reverse('document-list')
        file = SimpleUploadedFile('test.pdf', b'content', content_type='application/pdf')
        data = {'title': 'New Doc', 'file': file}
        response = admin_client.post(url, data, format='multipart')
        assert response.status_code == 201

    @patch('document.serializers.serializers.MinIOStorage')
    def test_editor_can_create_document(self, mock_storage, editor_client):
        mock_storage_instance = MagicMock()
        mock_storage_instance.upload_file.return_value = 'documents/test.pdf'
        mock_storage.return_value = mock_storage_instance
        
        url = reverse('document-list')
        file = SimpleUploadedFile('test.pdf', b'content', content_type='application/pdf')
        data = {'title': 'New Doc', 'file': file}
        response = editor_client.post(url, data, format='multipart')
        assert response.status_code == 201

    def test_viewer_cannot_create_document(self, viewer_client):
        url = reverse('document-list')
        file = SimpleUploadedFile('test.pdf', b'content', content_type='application/pdf')
        data = {'title': 'New Doc', 'file': file}
        response = viewer_client.post(url, data, format='multipart')
        assert response.status_code == 403

    @patch('document.serializers.serializers.MinIOStorage')
    def test_admin_can_update_document(self, mock_storage, admin_client, document):
        mock_storage_instance = MagicMock()
        mock_storage_instance.upload_file.return_value = 'documents/updated.pdf'
        mock_storage.return_value = mock_storage_instance
        
        url = reverse('document-detail', kwargs={'pk': document.pk})
        file = SimpleUploadedFile('updated.pdf', b'content', content_type='application/pdf')
        data = {'title': 'Updated', 'file': file}
        response = admin_client.put(url, data, format='multipart')
        assert response.status_code == 200

    @patch('document.serializers.serializers.MinIOStorage')
    def test_editor_can_update_document(self, mock_storage, editor_client, document):
        mock_storage_instance = MagicMock()
        mock_storage_instance.upload_file.return_value = 'documents/updated.pdf'
        mock_storage.return_value = mock_storage_instance
        
        url = reverse('document-detail', kwargs={'pk': document.pk})
        file = SimpleUploadedFile('updated.pdf', b'content', content_type='application/pdf')
        data = {'title': 'Updated', 'file': file}
        response = editor_client.put(url, data, format='multipart')
        assert response.status_code == 200

    def test_viewer_cannot_update_document(self, viewer_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        data = {'title': 'Updated'}
        response = viewer_client.put(url, data)
        assert response.status_code == 403

    def test_admin_can_partial_update_document(self, admin_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        data = {'title': 'Patched'}
        response = admin_client.patch(url, data)
        assert response.status_code == 200

    def test_editor_can_partial_update_document(self, editor_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        data = {'title': 'Patched'}
        response = editor_client.patch(url, data)
        assert response.status_code == 200

    def test_viewer_cannot_partial_update_document(self, viewer_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        data = {'title': 'Patched'}
        response = viewer_client.patch(url, data)
        assert response.status_code == 403

    def test_admin_can_delete_document(self, admin_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        response = admin_client.delete(url)
        assert response.status_code == 204

    def test_editor_cannot_delete_document(self, editor_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        response = editor_client.delete(url)
        assert response.status_code == 403

    def test_viewer_cannot_delete_document(self, viewer_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        response = viewer_client.delete(url)
        assert response.status_code == 403

    def test_superuser_bypasses_rbac(self, superuser_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        response = superuser_client.delete(url)
        assert response.status_code == 204
