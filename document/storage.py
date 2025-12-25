from minio import Minio
from minio.error import S3Error
from django.conf import settings
import uuid
from urllib3.exceptions import MaxRetryError, ProtocolError
from http.client import RemoteDisconnected


class MinIOStorage:
    _client = None
    _bucket_checked = False

    def __init__(self):
        self._get_client()
        self.bucket_name = settings.MINIO_BUCKET_NAME
        if not MinIOStorage._bucket_checked:
            self._ensure_bucket_exists()
            MinIOStorage._bucket_checked = True

    def _get_client(self):
        if MinIOStorage._client is None:
            MinIOStorage._client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_USE_HTTPS
            )
        self.client = MinIOStorage._client

    def _reset_connection(self):
        MinIOStorage._client = None
        MinIOStorage._bucket_checked = False
        self._get_client()

    def _retry_on_disconnect(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (MaxRetryError, ProtocolError, RemoteDisconnected, ConnectionError, OSError):
            self._reset_connection()
            return func(*args, **kwargs)

    def _ensure_bucket_exists(self):
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def upload_file(self, file_obj, file_name):
        unique_name = f"{uuid.uuid4()}_{file_name}"
        self._retry_on_disconnect(
            self.client.put_object,
            self.bucket_name,
            unique_name,
            file_obj,
            length=file_obj.size,
            content_type=file_obj.content_type
        )
        return unique_name

    def delete_file(self, file_path):
        self._retry_on_disconnect(self.client.remove_object, self.bucket_name, file_path)

    def get_file_url(self, file_path):
        return self._retry_on_disconnect(self.client.presigned_get_object, self.bucket_name, file_path)
