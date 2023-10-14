from django.db import models


class TelegramChannel(models.Model):
    username = models.CharField(max_length=32)

    def get_absolute_url(self):
        return f"https://www.t.me/{self.username}"

    def __str__(self):
        return f"TelegramChannel({self.username})"


class TelegramMessage(models.Model):
    class Meta:
        unique_together = [["message_id", "channel"]]

    text = models.TextField()
    datetime = models.DateTimeField()
    message_id = models.PositiveIntegerField()
    channel = models.ForeignKey(
        TelegramChannel,
        models.RESTRICT,
        related_name="messages",
    )

    def get_absolute_url(self):
        return f"https://www.t.me/{self.channel.username}/{self.message_id}"

    def __str__(self):
        return f"TelegramMessage({self.pk})"
