from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    try:
        if sender.name == 'account':
            from .models import RoleModel
            for role, _ in [('admin', 'Admin'), ('editor', 'Editor'), ('viewer', 'Viewer')]:
                RoleModel.objects.get_or_create(role_name=role)
    except Exception as e:
        print(f"Error creating default roles: {e}")
