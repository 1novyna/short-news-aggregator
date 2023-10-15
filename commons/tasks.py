from datetime import timedelta
from threading import Timer
from asgiref.sync import async_to_sync


class RepeatTimer(Timer):
    def __init__(
        self,
        interval: timedelta,
        function,
        is_async=False,
        args=None,
        kwargs=None,
    ):
        seconds = interval.total_seconds()
        if is_async:
            function = async_to_sync(function)
        super().__init__(seconds, function, args, kwargs)
        self.daemon = True

    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
