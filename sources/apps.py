from django.apps import AppConfig

from threading import Timer
from asgiref.sync import async_to_sync


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class SourcesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sources"

    def ready(self):
        self.start_background_task()

    def start_background_task(self):
        from .tasks import gather_messages

        thread = RepeatTimer(float(10 * 60), async_to_sync(gather_messages))
        thread.daemon = True
        thread.start()
