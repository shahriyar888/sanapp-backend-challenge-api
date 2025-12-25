from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('editor', 'Editor'),
    ('viewer', 'Viewer')

]


class RoleModel(models.Model):
    role_name = models.CharField(max_length=50, choices=ROLE_CHOICES, default='viewer')


def get_default_role():
    return RoleModel.objects.get_or_create(role_name='viewer')[0].id


class User(AbstractUser):
    role = models.ForeignKey(RoleModel, on_delete=models.PROTECT, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.role_id:
            viewer_role, _ = RoleModel.objects.get_or_create(role_name='viewer')
            self.role = viewer_role
        super().save(*args, **kwargs)
