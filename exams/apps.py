from django.apps import AppConfig
from django.conf import settings
from django.db.utils import OperationalError


class ExamsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exams'

    def ready(self):
        from .models import CustomUser
        try:
            if not CustomUser.objects.filter(role="admin").exists():
                CustomUser.objects.create_user(
                    username="admin",
                    password="admin123",   # default password
                    role="admin"
                )
                print("✅ Default Admin (username=admin, password=admin123) created!")
        except OperationalError:
            # happens during first migrate, ignore
            pass
