from django.db import models

from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import json


class EmbeddingField(models.TextField):
    def from_db_value(self, value, expression, connection):
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


class MessageQuerySet(models.QuerySet):
    def get_df_clusters(self):
        df = self.to_data_frame()
        n_clusters = self.get_approximate_clusters_number()

        kmeans = KMeans(n_clusters=n_clusters, init="k-means++", random_state=42)
        matrix = np.vstack(df.embedding.values)
        kmeans.fit(matrix)  # ValueError: could not convert string to float in embedding
        labels = kmeans.labels_
        df["cluster"] = labels

        df.groupby("cluster")
        clusters = self.get_df_clusters().to_dict()  #
        print(clusters)  #
        return df

    def to_data_frame(self):
        return pd.DataFrame(list(self.values()))

    def get_approximate_clusters_number(self):
        messages_number = self.aggregate(count=models.Count("id"))["count"]
        channels_number = self.aggregate(count=models.Count("channel"))["count"]
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
