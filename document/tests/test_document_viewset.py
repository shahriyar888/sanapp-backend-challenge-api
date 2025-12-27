import pytest
from django.urls import reverse
from unittest.mock import patch, MagicMock
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestDocumentViewSet:
    
    def test_list_documents_success_200(self, viewer_client, document):
        url = reverse('document-list')
        response = viewer_client.get(url)
        
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_search_documents_by_title(self, authenticated_client, document):
        url = reverse('document-list')
        response = authenticated_client.get(url, {'s': document.title})
        
        assert response.status_code == 200
        assert len(response.data) >= 1
        assert document.title in [doc['title'] for doc in response.data]

    def test_search_documents_by_description(self, authenticated_client, document):
        url = reverse('document-list')
        response = authenticated_client.get(url, {'s': document.description})
        
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_search_documents_by_filename(self, authenticated_client, document):
        url = reverse('document-list')
        response = authenticated_client.get(url, {'s': document.file_name})
        
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_search_documents_no_results(self, authenticated_client, document):
        url = reverse('document-list')
        response = authenticated_client.get(url, {'s': 'nonexistent'})
        
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_search_documents_empty_query(self, authenticated_client, document):
        url = reverse('document-list')
        response = authenticated_client.get(url, {'s': ''})
        
        assert response.status_code == 200
        assert len(response.data) >= 1

    def test_list_documents_unauthorized_401(self, api_client):
        url = reverse('document-list')
        response = api_client.get(url)
        
        assert response.status_code == 401

    def test_retrieve_document_success_200(self, viewer_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        response = viewer_client.get(url)
        
        assert response.status_code == 200
        assert response.data['id'] == document.id
        assert response.data['title'] == document.title

    def test_retrieve_document_not_found_404(self, viewer_client):
        url = reverse('document-detail', kwargs={'pk': 99999})
        response = viewer_client.get(url)
        
        assert response.status_code == 404

    def test_retrieve_document_unauthorized_401(self, api_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        response = api_client.get(url)
        
        assert response.status_code == 401

    @patch('document.tasks.upload_tasks.upload_document_to_minio.delay')
    def test_create_document_success_201(self, mock_task, editor_client):
        url = reverse('document-list')
        file = SimpleUploadedFile('test.pdf', b'file_content', content_type='application/pdf')
        data = {
            'title': 'New Document',
            'description': 'Test description',
            'file': file
        }
        response = editor_client.post(url, data, format='multipart')
        
        assert response.status_code == 201
        assert response.data['title'] == 'New Document'
        assert 'id' in response.data

    def test_create_document_missing_file_400(self, editor_client):
        url = reverse('document-list')
        data = {
            'title': 'New Document',
            'description': 'Test description'
        }
        response = editor_client.post(url, data)
        
        assert response.status_code == 400

    def test_create_document_missing_title_400(self, editor_client):
        url = reverse('document-list')
        file = SimpleUploadedFile('test.pdf', b'file_content', content_type='application/pdf')
        data = {'file': file}
        response = editor_client.post(url, data, format='multipart')
        
        assert response.status_code == 400

    def test_create_document_unauthorized_401(self, api_client):
        url = reverse('document-list')
        file = SimpleUploadedFile('test.pdf', b'file_content', content_type='application/pdf')
        data = {
            'title': 'New Document',
            'file': file
        }
        response = api_client.post(url, data, format='multipart')
        
        assert response.status_code == 401

    @patch('document.tasks.upload_tasks.upload_document_to_minio.delay')
    def test_update_document_success_200(self, mock_task, editor_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        file = SimpleUploadedFile('updated.pdf', b'new_content', content_type='application/pdf')
        data = {
            'title': 'Updated Document',
            'description': 'Updated description',
            'file': file
        }
        response = editor_client.put(url, data, format='multipart')
        
        assert response.status_code == 200
        assert response.data['title'] == 'Updated Document'

    def test_update_document_not_found_404(self, editor_client):
        url = reverse('document-detail', kwargs={'pk': 99999})
        file = SimpleUploadedFile('test.pdf', b'content', content_type='application/pdf')
        data = {
            'title': 'Updated',
            'file': file
        }
        response = editor_client.put(url, data, format='multipart')
        
        assert response.status_code == 404

    def test_partial_update_document_success_200(self, editor_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        data = {'title': 'Partially Updated'}
        response = editor_client.patch(url, data)
        
        assert response.status_code == 200
        assert response.data['title'] == 'Partially Updated'

    def test_partial_update_document_unauthorized_401(self, api_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        data = {'title': 'Updated'}
        response = api_client.patch(url, data)
        
        assert response.status_code == 401

    def test_delete_document_success_204(self, admin_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        response = admin_client.delete(url)
        
        assert response.status_code == 204

    def test_delete_document_not_found_404(self, admin_client):
        url = reverse('document-detail', kwargs={'pk': 99999})
        response = admin_client.delete(url)
        
        assert response.status_code == 404

    def test_delete_document_unauthorized_401(self, api_client, document):
        url = reverse('document-detail', kwargs={'pk': document.pk})
        response = api_client.delete(url)
        
        assert response.status_code == 401

    @patch('document.storage.MinIOStorage.get_file_url')
    def test_download_document_success_200(self, mock_get_url, viewer_client, document):
        mock_get_url.return_value = 'http://minio:9000/bucket/file.pdf?signed=true'
        document.status = 'COMPLETED'
        document.file_path = 'test-file.pdf'
        document.save()
        
        url = reverse('document-download', kwargs={'pk': document.pk})
        response = viewer_client.get(url)
        
        assert response.status_code == 200
        assert 'download_url' in response.data
        mock_get_url.assert_called_once_with('test-file.pdf')
