from django.db import models


class LogLevel(models.IntegerChoices):
    CRITICAL = 0, "Critical"
    ERROR = 1, "Error"
    WARNING = 2, "Warning"
    DEBUG = 3, "Debug"
    INFO = 4, "Info"


class Log(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    level = models.PositiveSmallIntegerField(choices=LogLevel.choices)
    message = models.TextField()

    def __str__(self):
        return f"Log({self.datetime})"
