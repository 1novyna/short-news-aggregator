from django.db import models


class Cluster(models.Model):
    digest = models.TextField(default="", blank=True)

    def __str__(self):
        return f"Cluster({self.id})"
