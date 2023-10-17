from django.db import models

from sklearn.cluster import KMeans
import numpy as np
import pandas as pd

from commons.models import EmbeddingField
from telegram_channels.models import Channel
from clusters.models import Cluster


class MessageQuerySet(models.QuerySet):
    def get_clusters(self):
        df = self.to_data_frame()
        n_clusters = self.get_approximate_clusters_number()

        kmeans = KMeans(n_clusters=n_clusters, init="k-means++", random_state=42)
        matrix = np.vstack(df.embedding.values)
        kmeans.fit(matrix)

        labels = kmeans.labels_
        df["cluster"] = labels
        df.groupby("cluster")

        return df

    def to_data_frame(self):
        values = list(self.values())
        return pd.DataFrame(values)

    def get_approximate_clusters_number(self):
        messages_number = self.aggregate(count=models.Count("id"))["count"]
        channels_number = self.aggregate(
            count=models.Count(
                "channel_id",
                distinct=True,
            )
        )["count"]
        return messages_number // channels_number


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

    objects = MessageQuerySet.as_manager()

    def get_absolute_url(self):
        return f"https://www.t.me/{self.channel.username}/{self.message_id}"

    def __str__(self):
        return f"Message({self.pk})"
