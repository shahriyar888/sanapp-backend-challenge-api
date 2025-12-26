import base64
from celery import shared_task
from django.core.files.base import ContentFile
from document.models import DocumentModel
from document.storage import MinIOStorage


@shared_task(bind=True, max_retries=3)
def upload_document_to_minio(self, document_id, file_data, file_name, file_size, content_type):
    try:
        document = DocumentModel.objects.get(id=document_id)
        document.status = 'PROCESSING'
        document.save(update_fields=['status'])

        file_bytes = base64.b64decode(file_data)
        file_obj = ContentFile(file_bytes, name=file_name)
        file_obj.size = file_size
        file_obj.content_type = content_type

        storage = MinIOStorage()
        file_path = storage.upload_file(file_obj, file_name)

        document.file_path = file_path
        document.status = 'COMPLETED'
        document.save(update_fields=['file_path', 'status'])

        return {'status': 'success', 'document_id': document_id}

    except DocumentModel.DoesNotExist:
        return {'status': 'error', 'message': 'Document not found'}
    except Exception as exc:
        document = DocumentModel.objects.get(id=document_id)
        document.status = 'FAILED'
        document.error_message = str(exc)
        document.save(update_fields=['status', 'error_message'])
        raise self.retry(exc=exc, countdown=60)
