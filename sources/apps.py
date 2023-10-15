from django.apps import AppConfig
from datetime import timedelta

from commons.tasks import RepeatTimer


class SourcesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sources"

    def ready(self):
        self.start_background_task()

    def start_background_task(self):
        from .tasks import gather_messages

        thread = RepeatTimer(timedelta(seconds=10), gather_messages, is_async=True)
        thread.start()
