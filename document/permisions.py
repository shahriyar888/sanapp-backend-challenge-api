from rest_framework.permissions import BasePermission

class DocumentPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        action_roles = view.action_roles
        if view.action not in action_roles.keys():
            raise Exception('Action {} is not defined'.format(view.action))
        user_role = request.user.role.role_name if request.user.role else None
        if user_role in action_roles[view.action]:
            return True
        else:
            return False
