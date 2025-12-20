from minio import Minio
from minio.error import S3Error
from django.conf import settings
import uuid


class MinIOStorage:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_USE_HTTPS
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error:
            pass

    def upload_file(self, file_obj, file_name):
        unique_name = f"{uuid.uuid4()}_{file_name}"
        self.client.put_object(
            self.bucket_name,
            unique_name,
            file_obj,
            length=file_obj.size,
            content_type=file_obj.content_type
        )
        return unique_name

    def delete_file(self, file_path):
        try:
            self.client.remove_object(self.bucket_name, file_path)
        except S3Error:
            pass

    def get_file_url(self, file_path):
        return self.client.presigned_get_object(self.bucket_name, file_path)
