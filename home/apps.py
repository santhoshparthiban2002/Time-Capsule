from django.apps import AppConfig
from django.conf import settings

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from timecapsule import scheduler