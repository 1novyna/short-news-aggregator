from django.db import models

from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import json


class EmbeddingField(models.TextField):
    def to_python(self, value):
        return json.loads(value)

    def get_prep_value(self, value):
        if value:
            return json.dumps(value)


class Channel(models.Model):
    username = models.CharField(max_length=32)
    channel_id = models.PositiveIntegerField()

    def get_absolute_url(self):
        return f"https://www.t.me/{self.username}"

    def __str__(self):
        return f"Channel({self.username})"


class Cluster(models.Model):
    digest = models.TextField(default="", blank=True)

    def __str__(self):
        return f"Cluster({self.id})"


class Message(models.Model):
    class Meta:
        unique_together = [["message_id", "channel"]]

    text = models.TextField()
    datetime = models.DateTimeField()
    message_id = models.PositiveIntegerField()
    channel = models.ForeignKey(
        Channel,
        models.RESTRICT,
        related_name="messages",
    )
    embedding = EmbeddingField(blank=True, null=True)
    cluster = models.ForeignKey(
        Cluster,
        models.RESTRICT,
        related_name="messages",
        blank=True,
        null=True,
    )

    def get_absolute_url(self):
        return f"https://www.t.me/{self.channel.username}/{self.message_id}"

    def __str__(self):
        return f"Message({self.pk})"
