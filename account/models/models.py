from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('editor', 'Editor'),
    ('viewer', 'Viewer')

]


class RoleModel(models.Model):
    role_name = models.CharField(max_length=50, choices=ROLE_CHOICES, default='viewer')
    def __str__(self):
        return self.role_name


def get_default_role():
    return RoleModel.objects.get_or_create(role_name='viewer')[0].id


class User(AbstractUser):
    role = models.ForeignKey(RoleModel, on_delete=models.PROTECT, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.role_id:
            viewer_role, _ = RoleModel.objects.get_or_create(role_name='viewer')
            self.role = viewer_role
        if not self.is_staff:
            self.is_staff = True
        super().save(*args, **kwargs)

        def __str__(self):
            return f"{self.username} ({self.role})"
