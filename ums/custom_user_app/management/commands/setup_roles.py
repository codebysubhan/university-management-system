from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

class Command(BaseCommand):
    help = "Setup default roles and permissions"

    def handle(self, *args, **kwargs):
        roles = {
            "Admin": {"Student": ["add", "change", "delete", "view"]},
            "Faculty": {"Student": ["view", "change"]},
            "Student": {"Student": ["view"]},
        }

        for role_name, model_perms in roles.items():
            group, _ = Group.objects.get_or_create(name=role_name)
            for model_name, perms in model_perms.items():
                model = apps.get_model("custom_user_app", model_name)
                for perm_code in perms:
                    codename = f"{perm_code}_{model._meta.model_name}"
                    try:
                        permission = Permission.objects.get(codename=codename)
                        group.permissions.add(permission)
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Permission {codename} not found"))
        self.stdout.write(self.style.SUCCESS("Roles and permissions setup complete."))
